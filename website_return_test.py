tournament_id = 445
email = 'jtr.python@gmail.com'

url = 'https://turniere.jugger.org/tournament.php?id='+str(tournament_id)

import mechanize
import webbrowser


br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots

# solve captcha
response = br.open(url)

# response.read() == string
# keine line breaks drin (\n oder so) -> mist, brauche ich um wenigstens etwas zu parsen? .split() geht trotzdem
response_words = response.read().split()

target_string = 'name="google-site-verification"'
for i in range(len(response_words)):
    #print(response_words[i])
    try:
        if response_words[i] == target_string:
            print(response_words[i+1])
            break
    except:
        continue
