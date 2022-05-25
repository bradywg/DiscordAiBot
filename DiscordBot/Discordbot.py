import os
import gtts
import lightbulb
import hikari
from songbird import ffmpeg
from songbird.hikari import Voicebox

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY") #supply your openAI api key in the .ens file
Question=""

bot = lightbulb.BotApp(token= os.getenv("DISCORD_TOKEN"),prefix="!")#supply your discord bot token in the .ens file


#generates the response
def generate_prompt(Question):
    return """Have a conversation but be sarcastic.
question: What is your name?
Respond: Brady
question: How is it going?
Respond: Would be better if you left me alone
question: what time is it?
Respond: Time to get a watch
question: {}
Respond:""".format(
        Question.capitalize()
    )



@bot.command
@lightbulb.command("afk","Adds the ai to VC and starts chatting")
@lightbulb.implements(lightbulb.PrefixCommand)
async def afk(ctx: lightbulb.Context)-> None:
   vstate = ctx.bot.cache.get_voice_state(ctx.get_guild(), ctx.author.id)#gets the voice channel of the user who sent the command
   voice = await Voicebox.connect(bot, ctx.get_guild(), vstate.channel_id) #joins the bot to that voice channel
   while(True): # loops forever until another command is called
      await getResponse()
      await voice.play_source(await ffmpeg("C:/Users/Brady/Documents/music/Response.mp3"))

   

@bot.command
@lightbulb.command("back","Removes the ai from VC")
@lightbulb.implements(lightbulb.PrefixCommand)
async def back(ctx: lightbulb.Context)-> None:
   await ctx.bot.voice.disconnect(ctx.get_guild())


@bot.command
@lightbulb.command("end","Closes the bot")
@lightbulb.implements(lightbulb.PrefixCommand)
async def end(ctx: lightbulb.Context)-> None:
   await ctx.bot.close()


#generates the ai's response based off the users message
async def getResponse():
   talking =await bot.wait_for(hikari.GuildMessageCreateEvent,timeout=1000) #waits for users message
   Question =talking.content #gets the contents of the message 
   answer = openai.Completion.create( 
      engine="text-davinci-002",
      prompt=generate_prompt(Question),
      temperature=0.6,
      )
   talk = answer.choices[0].text 
   tts= gtts.gTTS(talk) #generates the text to speach
   tts.save("C:/Users/Brady/Documents/music/Response.mp3")#saves the mp3 file so it can be read later

bot.run()

