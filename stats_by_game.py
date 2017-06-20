import scrapy
import collections

class CricbaySpider(scrapy.Spider):
  name = 'cricbay_spider'
  start_urls = [
    'http://www.cricbay.com/a_teamroster.asp?teamId=192&seasonEventId=61&cbPID='
  ]
  players = dict()
  games = {}

  def parse_player_page(self, response):
    name = str(response.css('h1::text').extract_first())
    no_of_matches = 0

    odd_games = response.css('tr.cb-oddRow') or []
    even_games = response.css('tr.cb-evenRow') or []

    games_played = odd_games + even_games

    for game in games_played:
      title = str(game.css('td')[3].css('a::text').extract_first())

      if title == 'None':
        continue

      if title not in self.games:
        self.games[title] = [name]
      else:
        self.games[title].append(name)
        

    self.players[str(name)] = int(no_of_matches)
    yield self.games



  def parse(self, response):
    for player_link in response.css('div.cb-team-roster-grid > ul > li > h4 > a::attr(href)'):
      print player_link
      player_page = player_link.extract()
      if player_page is not None:
        player_page = response.urljoin(player_page)
        yield scrapy.Request(player_page, callback=self.parse_player_page)
