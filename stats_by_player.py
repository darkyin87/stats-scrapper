import scrapy
import collections

class CricbaySpider(scrapy.Spider):
  name = 'cricbay_spider'
  start_urls = [
    'http://www.cricbay.com/a_teamroster.asp?teamId=192&seasonEventId=61&cbPID='
  ]
  players = dict()

  def parse_player_page(self, response):
    name = response.css('h1::text').extract_first()
    no_of_matches = 0
    for stats in response.css('div.cb-career-stats'):
      title = stats.css('h3::text').extract_first()
      if title == 'Tournament Statistics':
        no_of_matches = stats.css('table tr')[1].css('td::text')[0].extract()

    self.players[str(name)] = int(no_of_matches)
    yield self.players



  def parse(self, response):
    for player_link in response.css('div.cb-team-roster-grid > ul > li > h4 > a::attr(href)'):
      print player_link
      player_page = player_link.extract()
      if player_page is not None:
        player_page = response.urljoin(player_page)
        yield scrapy.Request(player_page, callback=self.parse_player_page)
