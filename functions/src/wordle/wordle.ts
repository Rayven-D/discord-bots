import { Client, TextChannel } from "discord.js";
import * as functions from 'firebase-functions';

const firebaseConfig = functions.config();


export const sendWordleWarriors = functions.pubsub.schedule('0 0 * * *').timeZone("America/Chicago").onRun( () => {
    const client = new Client({
        intents: ["GUILDS", "GUILD_MESSAGES"],
    });

    client.login(firebaseConfig.wordle_bot.key);

    client.on('ready', () => {
        (client.channels.cache.get("943314950678515833") as TextChannel).send('<@&951348943407697930>')
    });
})