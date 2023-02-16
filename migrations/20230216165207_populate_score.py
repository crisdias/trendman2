"""
This module contains a Caribou migration.

Migration Name: populate_score 
Migration Version: 20230216165207
"""

GOOD_ARTICLES = [
    'https://authorsguild.org/news/amazon-changing-ebook-return-policy/',
    'https://www.wired.com/story/the-scramble-to-save-twitters-research-from-elon-musk/',
    'https://mastodon.social/@rjj/109870041441774034',
    'https://gizmodo.com/twitter-twitter-down-elon-musk-tweet-down-detector-1850119637',
    'https://www.businessinsider.com/marc-andreessen-remote-work-not-good-life-for-young-workers-2023-2',
    'https://freethoughtblogs.com/pharyngula/2023/02/15/i-agree-with-blake-stacey/',
    'https://www.disconnect.blog/p/tech-was-supposed-to-make-cars-safer',
    'https://www.wired.com/story/east-palestine-ohio-train-derailment-tiktok/',
    'https://www.theverge.com/2018/8/28/17777330/internet-of-garbage-book-sarah-jeong-online-harassment',
    'https://www.theregister.com/2023/02/15/digitalocean_layoffs/',
    'https://arstechnica.com/gaming/2023/02/prototype-of-the-final-unreleased-3dfx-gpu-sells-on-ebay-for-15000/',
    'https://www.techdirt.com/2023/02/15/engineers-gave-elons-tweets-special-treatment-because-elon-freaked-out-that-a-joe-biden-tweet-got-more-engagement/',
    'https://arstechnica.com/information-technology/2023/02/meta-develops-an-ai-language-bot-that-can-use-external-software-tools/',
    'https://fortune.com/2023/02/15/mansplaining-women-question-workplace-competence-stunt-careers/',
    'https://gizmodo.com/google-ai-bard-chatgpt-bing-openai-1850119138',
    'https://www.theverge.com/23601599/lego-bts-dynamite-music-video-set-release-date-price',
    'https://www.forbes.com/sites/evaamsen/2023/02/15/with-the-right-music-this-will-only-hurt-a-little-bit/',
    'https://www.theverge.com/2023/2/16/23602335/microsoft-bing-ai-testing-learnings-response',
    'https://www.wired.com/story/chatbots-got-big-and-their-ethical-red-flags-got-bigger/',
    'https://arstechnica.com/science/2023/02/a-quantum-computer-that-has-an-alternative-problem-solving-mode/',
    'https://www.wired.com/story/living-under-gravitys-rainbow-thomas-pynchon/',




]

BAD_ARTICLES = [
    'https://www.texasobserver.org/3-million-whistleblower-settlement-is-cheap-getaway-for-ken-paxton/',
    'https://prospect.org/power/proposed-kroger-albertsons-merger-would-create-grocery-giant/',
    'https://www.theverge.com/23599332/apple-watch-remote-control-how-to',
    'https://www.bbc.co.uk/news/uk-england-london-64641426',
    'https://variety.com/2023/film/news/raquel-welch-dead-one-million-years-bc-three-musketeers-actor-1235524180/',
    'https://www.msnbc.com/rachel-maddow-show/maddowblog/ignoring-mcconnell-rick-scott-pushes-controversial-entitlement-plan-rcna70759',
    'https://www.bbc.com/news/world-us-canada-64657781',
    'https://www.statnews.com/pharmalot/2023/02/15/covid19-vaccine-moderna-pfizer-sanders/',
    'https://grist.org/accountability/derailed-train-cars-ohio-not-labeled-toxic-cargo/',
    'https://www.theregister.com/2023/02/15/intel_sgx_vulns/',
    'https://www.democracydocket.com/news-alerts/u-s-senate-confirms-100th-federal-judge-nominated-by-president-joe-biden/',
    'https://apnews.com/article/biden-proud-boys-washington-law-enforcement-capitol-siege-07b606c578399a4e24cc382a17f6f470',
    'https://slate.com/news-and-politics/2023/02/wisconsin-supreme-court-justice-coup-challenge-story.html',
    'https://www.bbc.co.uk/news/world-asia-china-64658729',
    'https://abcnews.go.com/Health/moderna-covid-vaccine-remain-free-consumers-uninsured/story?id=97226324',
    'https://www.theregister.com/2023/02/16/doj_deere_repair/',
    'https://www.theregister.com/2023/02/16/electric_vehicle_chargers/',
    'https://www.bbc.co.uk/news/business-64652142',
    'https://www.politico.eu/article/uk-home-office-backs-down-in-legal-battle-over-eu-residents-rights/',
    'https://arstechnica.com/science/2022/12/the-moon-landing-was-faked-and-wind-farms-are-bad/',
    'https://www.bbc.co.uk/news/world-europe-64637928',
    'https://theconversation.com/insects-are-vanishing-worldwide-now-its-making-it-harder-to-grow-food-199826',
    'https://noahberlatsky.substack.com/p/why-white-students-need-black-history',
    'https://www.reuters.com/graphics/GLOBAL-ENVIRONMENT/INSECT-APOCALYPSE/egpbykdxjvq/',




]


def upgrade(connection):
    # add your upgrade step here
    cursor = connection.cursor()

    for article in GOOD_ARTICLES:
        item = cursor.execute("SELECT * FROM processed WHERE url = ?", (article,)).fetchone()
        if item:
            cursor.execute("UPDATE processed SET score = 1 WHERE url = ?", (article,))

    for article in BAD_ARTICLES:
        item = cursor.execute("SELECT * FROM processed WHERE url = ?", (article,)).fetchone()
        if item:
            cursor.execute("UPDATE processed SET score = 0 WHERE url = ?", (article,))
    

def downgrade(connection):
    # add your downgrade step here
    pass
