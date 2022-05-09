import { Client, MessageEmbed, TextChannel } from "discord.js";
import { initializeApp } from "firebase/app";
import {  collection, getDocs, getFirestore, query, } from 'firebase/firestore'
import { UserStats } from "./models/wordle-models";
//import * as functions from 'firebase-functions';

//const firebaseConfig = functions.config();

const firebaseConfig = {
    apiKey: "AIzaSyBPOPviJ7mOUAER5g5DVCtNa4qdxv4oX8s",
    authDomain: "wordle-bot-discord.firebaseapp.com",
    projectId: "wordle-bot-discord",
    storageBucket: "wordle-bot-discord.appspot.com",
    messagingSenderId: "734320513951",
    appId: "1:734320513951:web:03256eebebdc8713fd63aa",
    measurementId: "G-X2GWX1Y355"
  };


const client = new Client({
    intents: ["GUILDS", "GUILD_MESSAGES"],
});

// client.login(firebaseConfig.wordle_bot.key);

const app = initializeApp(firebaseConfig)
const db = getFirestore(app);

client.login('OTU1MzA4NDE0NjYwMTIwNTg2.YjfySg.OnBvh42Egeahzsyx5eJrp6V_OcQ')

client.on('ready', async () => {
    const channel = client.channels.cache.get("943314950678515833") as TextChannel
    //channel.send('<@&951348943407697930>')
    

    // let startMessage = await channel.messages.fetch({limit: 1, before: '973087007653912636'});
    // let message = startMessage.size === 1 ?  startMessage.at(0) : null;
    // let yesterdayMessages: Message[] = []
    // while(message){
    //     let messages = await channel.messages
    //         .fetch({limit: 100, before: message.id})
    //     messages.forEach(msg =>{ yesterdayMessages.push(msg)})
    //     message = 0 < messages.size ? messages.at(messages.size - 1) : null;
    //     console.log(yesterdayMessages.length)
    // }   
    // let wordleMessages: Message[] = []
    // yesterdayMessages.forEach( (msg)=>{
    //     if(msg.content.match(/Wordle [0-9]\d+/)){
    //         wordleMessages.push(msg);
    //     }
    // })
    // wordleMessages.sort( (a,b)=>{
    //     let a_time = a.createdAt
    //     let b_time = b.createdAt
    //     return a_time > b_time ? 1 : -1;
    // })
    // for( let msg of wordleMessages){
    //     console.log(msg.content.split(" ")[1])
       
    //     // console.log(numTries + msg.author.username)
        
    //     let docRef = doc(db, "Users", msg.author.id);
    //     let docSnap = await getDoc(docRef);
    //     if(docSnap.exists()){
    //         if(docSnap.metadata.hasPendingWrites){
    //             console.log()
    //             docSnap = await getDoc(docRef);
    //         }
    //         let numTries = msg.content.split(' ').find(str => str.includes('/'))!.charAt(0)
    //         let user: UserStats = docSnap.data() as UserStats;
    //         let index = -1;
    //         if(numTries.match(/[1-6]/)){
    //             index = +numTries;
    //             index--;
    //         }
    //         else{
    //             index = 6
    //         }
    //         user.tries[index]++;

    //         await updateDoc(docRef, {
    //             tries: user.tries
    //         })
    //     }else{
    //         let numTries = msg.content.split(' ')[2].split('/')[0];

    //         let user: UserStats = {
    //             id: msg.author.id,
    //             username: msg.author.username,
    //             tries: [0,0,0,0,0,0,0]
    //         }
    //         let index = -1;
    //         if(numTries.match(/[1-6]/)){
    //             index = +numTries;
    //             index--;
    //         }
    //         else{
    //             index = 6
    //         }

    //         user.tries[index]++;
    //         await setDoc(docRef, user);
    //     }
    // }

    let col = collection(db, 'Users');
    let q = query(col)

    let qSnap = await getDocs(q);
    if(!qSnap.empty){
        const users: UserStats[] =[]
        qSnap.forEach( snap =>{ 
            users.push(snap.data() as UserStats)
        })
        

        users.forEach(user =>{
            const chart = {
                type: 'horizontalBar',
                data:{
                    labels:['1', '2', '3', '4','5','6','X'],
                    datasets:[{
                        label: 'Tries',
                        data: user.tries
                    }]
                },
                options:{
                    plugins: {
                        datalabels: {
                          anchor: 'center',
                          align: 'center',
                          color: '#FFF',
                          font: {
                            weight: 'normal',
                          },
                        },
                      }
                }
            }

            const encodedChart = encodeURIComponent(JSON.stringify(chart))
            const chartURL = `https://quickchart.io/chart?c=${encodedChart}&bkg=white`;

 

            const embed = new MessageEmbed();
            embed.setTitle(`${user.username} Wordle Stats`);
            embed.setDescription('')
            embed.setImage(chartURL)
            embed.setColor('GREEN')

            channel.send({embeds: [embed]})
        })
    }

});