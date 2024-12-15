
<script module>
    

</script>

<script lang='ts'>
    import { browser } from '$app/environment'; 
    import { io } from "socket.io-client";
    import {marked} from 'marked'

    import type { Message } from '../components/ChatMessage.svelte'
    import ChatMessage from '../components/ChatMessage.svelte'
    import ChatInput from '../components/ChatInput.svelte';

    let {data} = $props()

    // Server variables 
    const socket_url = "http://127.0.0.1:5000/"; 
    const socket = io(socket_url);

    // State variables
    let allowSend = $state(true)
    let lastElement = $state<null|HTMLElement>(null)
    let fileInput = $state<null|HTMLInputElement>(null)
    let fileAvailable = $state(false)
    let messageList = $state<Message[]>([])   


    $effect(() => {
        if(lastElement) {
            lastElement.scrollIntoView({behavior: 'smooth'})
        }
	});


// Function to get a cookie by name
    function getCookie(cname: string) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');

  // Loop through the cookies and return the value of the cookie with the name 'cname'
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// Function to uppload a file
    function onFileChange(event: Event) {
        const file = (event.target as HTMLInputElement).files?.[0]
        const formData = new FormData()
        formData.append('file', file as Blob, file?.name as string)
        if(file && browser) {
             fetch(socket_url + `documents/${getCookie('session')}`, {
            method: 'POST',
            body: formData
        }).then(repsonse => {
            console.log(repsonse)
            messageList.push({text: `Uploaded ${file.name}`, sentBy: "info", sentAt: new Date(), file: file})
            fileAvailable ? null : fileAvailable = true
        }).catch(error => {
            console.log(error)
        })
            
        }
    }   

    // Function to send a message to the server
    function sendMessage(search: string, searchingEnabled: boolean) {
        // Either send a regular message or search for information in a document
        socket.emit('send_message', search, searchingEnabled);
        messageList.push({text: search, sentBy: "user", sentAt: new Date()})
        allowSend = false
    }

    
    // Handle a response from the server 
    socket.on("new_message", ({content}) => {
        messageList.push({text: content, sentBy: "ai", sentAt: new Date()})
        allowSend = true
    })

   
    // Handle the session id cookie. TODO: Change to a session id connected to the users Google account
    socket.on('cookie', (cookie) => {
        console.log(cookie)
        if(browser) {
            let getTommorow = () => {
                let date = new Date();
                date.setDate(date.getDate() + 1);
                return date;
            }
            // Set the session cookie to the session id received from the server
            document.cookie = `session=${cookie['SSID']}; expires=${getTommorow()}; path=/`
        }
    })

    // Delete the session cookie when the user disconnects
    socket.on('disconnect', () => {
        console.log('disconnected')
        if(browser) {
            document.cookie = `session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`
        }
    })    
            
</script>


<div class="h-screen flex flex-col">
<h1 class=" text-center text-3xl p-20">Börja undersöka dina dokument</h1>
<div class="w-full h-full flex flex-col items-center justify-end pb-10 ">
    <div class="w-[800px] h-full flex flex-col items-center justify-end">
        <div class="w-full h-[70vh] flex flex-col overflow-y-scroll auto scrollbar-hidden" >
        <!-- Loop through the messages and display them -->
        {#each messageList as message, i}
        <!-- Store the last message in lastElement so it can easily be scrolled to -->
        {#if i == messageList.length - 1}
        <div class="w-full" bind:this={lastElement}>
            <ChatMessage message={message}/>
        </div>
        {:else}
        <ChatMessage message={message} />
        {/if}
    {/each}
    </div>
    <ChatInput fileInput={fileInput} onFileChange={onFileChange} sendMessage={sendMessage} allowSend={allowSend} />
    </div>
   
</div>
</div>

