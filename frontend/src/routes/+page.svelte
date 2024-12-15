
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


    const socket_url = "http://127.0.0.1:5000/"; // does not work at the moment, needs to be changed to the server's url
    const socket = io(socket_url);
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

    

    

    

    function getCookie(cname: string) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
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

    function searchDocument(search: string, searchingEnabled: boolean) {
        socket.emit('send_message', search, searchingEnabled);
        messageList.push({text: search, sentBy: "user", sentAt: new Date()})
        allowSend = false
    }

    
    socket.on("new_message", ({content}) => {
        messageList.push({text: content, sentBy: "ai", sentAt: new Date()})
        allowSend = true
    })

   
    socket.on('cookie', (cookie) => {

        console.log(cookie)
        if(browser) {
            let getTommorow = () => {
                let date = new Date();
                date.setDate(date.getDate() + 1);
                return date;
            }
            document.cookie = `session=${cookie['SSID']}; expires=${getTommorow()}; path=/`
        }
    })

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
        {#each messageList as message, i}
        {#if i == messageList.length - 1}
        <div class="w-full" bind:this={lastElement}>
            <ChatMessage message={message}/>
        </div>
        {:else}
        <ChatMessage message={message} />
        {/if}
    {/each}
    </div>
    <ChatInput fileInput={fileInput} onFileChange={onFileChange} searchDocument={searchDocument} />
    </div>
   
</div>
</div>

