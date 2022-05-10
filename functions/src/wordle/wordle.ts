import { Client, Message, TextChannel } from "discord.js";
import { initializeApp } from "firebase/app";
import * as functions from 'firebase-functions';
import { doc, getDoc, getFirestore,  setDoc, updateDoc } from "firebase/firestore";
import { LastCallMessage, UserStats } from "../models/wordle-models";

const firebaseConfig = functions.config();

const firebaseAppConfig = {
    apiKey: "AIzaSyBPOPviJ7mOUAER5g5DVCtNa4qdxv4oX8s",
    authDomain: "wordle-bot-discord.firebaseapp.com",
    projectId: "wordle-bot-discord",
    storageBucket: "wordle-bot-discord.appspot.com",
    messagingSenderId: "734320513951",
    appId: "1:734320513951:web:03256eebebdc8713fd63aa",
    measurementId: "G-X2GWX1Y355"
  };


export const sendWordleWarriors = functions.pubsub.schedule('0 0 * * *').timeZone("America/Chicago").onRun( () => {
    const client = new Client({
        intents: ["GUILDS", "GUILD_MESSAGES"],
    });

    client.login(firebaseConfig.wordle_bot.key);


    client.on('ready', async () => {
        const app = initializeApp(firebaseAppConfig)
        const db = getFirestore(app);
        const channel = client.channels.cache.get("943314950678515833") as TextChannel       
        let newCallMsg = await channel.send('<@&951348943407697930>') //ping @Wordle Warrios


        const docRef = doc(db, 'LastCallMessage', 'lastcall')
        const lastCall: LastCallMessage = (await getDoc(docRef)).data() as LastCallMessage
        
        let yesderdayMessages = await channel.messages.fetch({after: lastCall.lastID});
        await updateDoc(docRef, {
            lastID: newCallMsg.id
        })
        let wordleMessages: Message[] = []
        yesderdayMessages.forEach( (msg)=>{
            if(msg.content.match(/Wordle [0-9]\d+/)){
                wordleMessages.push(msg);
            }
        })
        wordleMessages.sort( (a,b)=>{
            let a_time = a.createdAt
            let b_time = b.createdAt
            return a_time > b_time ? 1 : -1;
        })
        
        for( let msg of wordleMessages){
            
            let docRef = doc(db, "Users", msg.author.id);
            let docSnap = await getDoc(docRef);
            if(docSnap.exists()){
                if(docSnap.metadata.hasPendingWrites){
                    console.log()
                    docSnap = await getDoc(docRef);
                }
                let numTries = msg.content.split(' ').find(str => str.includes('/'))!.charAt(0)
                let user: UserStats = docSnap.data() as UserStats;
                let index = -1;
                if(numTries.match(/[1-6]/)){
                    index = +numTries;
                    index--;
                }
                else{
                    index = 6
                }
                user.tries[index]++;
    
                await updateDoc(docRef, {
                    tries: user.tries
                })
            }else{
                let numTries = msg.content.split(' ').find(str => str.includes('/'))!.charAt(0)
    
                let user: UserStats = {
                    id: msg.author.id,
                    username: msg.author.username,
                    tries: [0,0,0,0,0,0,0]
                }
                let index = -1;
                if(numTries.match(/[1-6]/)){
                    index = +numTries;
                    index--;
                }
                else{
                    index = 6
                }
    
                user.tries[index]++;
                await setDoc(docRef, user);
            }
        }
    });
})