from celery import shared_task
import urllib.parse
from datetime import datetime
from requests_html import HTMLSession
from wave_proj.wave_scraper.models import Article, Task
import logging

logger = logging.getLogger(__name__)


def get_tags_by_class(tags, css_class):
    tag_list = []
    for tag in tags:
        if tag and 'class' in tag.attrs and css_class in tag.attrs['class']:
            tag_list.append(tag)
    return tag_list


def get_specific_tag_text(tags, position):
    try:
        if len(tags) > position:
            return tags[position].text.strip()
    except AttributeError:
        return None


@shared_task
def scraper(pages):
    try:
        task = Task()
        task.task_id = str(scraper.request.id)
        task.started_at = datetime.now()
        task.save()
        session = HTMLSession()
        base_url = "https://www.your_test_blog_here.com"
        for page_number in range(1, pages + 1):
            logger.info("Scraping page {0} of {1}".format(page_number, pages + 1))
            url = '{base_url}/blog?page={page_number}'.format(base_url=base_url, page_number=page_number)
            page = session.get(url)
            page.html.render()

            read_more_buttons = page.html.find('a', first=False)

            button_tags = get_tags_by_class(read_more_buttons, 'read-more')
            for button in button_tags:
                if 'href' in button.attrs and button.attrs['href']:
                    link = button.attrs['href']
                else:
                    continue
                article = session.get(urllib.parse.urljoin(base_url, link))
                article.html.render()

                titles = article.html.find('h1', first=False)
                title_tag = get_tags_by_class(titles, 'article-title')
                title = get_specific_tag_text(title_tag, 0)

                authors = article.html.find('div', first=False)
                author_tag = get_tags_by_class(authors, 'name')
                author = get_specific_tag_text(author_tag, 0)

                crumbs = article.html.find('span', first=False)
                category_tag = get_tags_by_class(crumbs, 'link-breadbrumbs')
                category = get_specific_tag_text(category_tag, 1)

                contents = article.html.find('div', first=False)
                content_tag = get_tags_by_class(contents, 'the-content')
                full_content = get_specific_tag_text(content_tag, 0)

                if title and author and category and full_content:
                    logger.info("Article {0} scraped".format(title))
                    new_article = Article()
                    new_article.title = title
                    new_article.author = author
                    new_article.category = category
                    new_article.content = full_content
                    new_article.save()
        task.completed_at = datetime.now()
        task.status = "SUCCESS"
        task.save()
        session.close()
        return "Articles Loaded"
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        task = Task.objects.get(task_id=str(scraper.request.id))
        task.completed_at = datetime.now()
        task.status = "FAILED"
        task.save()
        return message
