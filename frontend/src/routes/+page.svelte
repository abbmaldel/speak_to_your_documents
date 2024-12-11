


<script lang='ts'>
    import { browser } from '$app/environment'; 
    import { io } from "socket.io-client";
    import {marked} from 'marked'
    let {data} = $props()


    const socket_url = "http://127.0.0.1:5000/"; // does not work at the moment, needs to be changed to the server's url
    const socket = io(socket_url);
    let search = $state('')
    let allowSend = $state(true)
    let lastElement = $state<null|HTMLElement>(null)
    let fileInput = $state<null|HTMLInputElement>(null)
    let fileAvailable = $state(false)
    let searchingEnabled = $state(false)
    let commandMode = $state(false)

    let messageList = $state<{ text: string, sentBy: "user"|"ai"|"info", sentAt: Date, file?:  any}[]>([])


    $effect(() => {
        if(lastElement) {
            lastElement.scrollIntoView({behavior: 'smooth'})
        }
	});

    

    

    function uploadFile() {
        if(fileInput) {
            fileInput.click()    
        }
    }

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

    function searchDocument() {
        socket.emit('send_message', search, searchingEnabled);
        messageList.push({text: search, sentBy: "user", sentAt: new Date()})
        search = ''
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




    function onkeyenter(event: KeyboardEvent) {
    console.log(event)
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault()
        if(allowSend) {
           searchDocument()
            
            }

            }
}

    
            
</script>


<div class="h-screen flex flex-col">
<h1 class=" text-center text-3xl p-20">Börja undersöka dina dokument</h1>
<div class="w-full h-full flex flex-col items-center justify-end pb-10 ">
    <div class="w-[800px] h-full flex flex-col items-center justify-end">
        <div class="w-full h-[70vh] flex flex-col overflow-y-scroll auto scrollbar-hidden" >
        {#each messageList as message, i}
        {#if i == messageList.length - 1}
        <div class={`flex flex-col   my-1 ${message.sentBy === "user" ? 'self-end items-end ' : message.sentBy === 'info' ? 'self-center items-center' :  'self-start items-start '}`} bind:this={lastElement}>
            <p class="text-gray-500 text-sm">{message.sentAt.toLocaleTimeString([],{timeStyle: "short"})}</p>
        <div class={`rounded-3xl px-3 flex flex-row items-center justify-between py-2 prose ${message.sentBy === "user" ? ' bg-red-500 text-white' : message.sentBy === "info" ? 'text-sm text-gray-500' :  'bg-white-300 border border-black text-black'}`}>
            {#if message.file}
            <p>
                {message.text}
                <a href={URL.createObjectURL(message.file)} download={message.file.name} class=" underline">View </a>
            </p>            
            {:else}
            <p>{@html marked(message.text)}</p>
            {/if}
        </div>
        </div>
        {:else}
        <div class={`flex flex-col   my-1 ${message.sentBy === "user" ? 'self-end items-end ' : message.sentBy === 'info' ? 'self-center items-center' :  'self-start items-start '}`}>
            <p class="text-gray-500 text-sm">{message.sentAt.toLocaleTimeString([],{timeStyle: "short"})}</p>
        <div class={`rounded-3xl px-3 flex flex-row items-center justify-between py-2 prose  ${message.sentBy === "user" ? ' bg-red-500 text-white' : message.sentBy === "info" ? 'text-sm text-gray-500' :  'bg-white-300 border border-black text-black'}`}>
            {#if message.file}
            <p>
                {message.text}
                <a href={URL.createObjectURL(message.file)} download={message.file.name} class=" underline">View </a>
            </p>
            {:else}
            <p>{@html marked(message.text)}</p>
            {/if}
        </div>
        </div>
        {/if}
    {/each}
    </div>
    <div class="w-full flex flex-row items-center">
    <input type="file" id="file" name="file" accept=".pdf" class="hidden" bind:this={fileInput}  onchange={onFileChange}/>
    <button class=" text-gray-500 rounded-3xl h-9 w-1/12" onclick={() => uploadFile()} >+</button>
    <div class="border border-gray-300 rounded-3xl px-3 w-full flex flex-row items-center justify-between py-2 ">
        <p id="search" onkeydown={onkeyenter} contenteditable bind:innerText={search} class=" w-10/12 outline-none" ></p>
        <p class={search.length==0 ? ' block absolute -z-10 text-gray-500' : 'hidden'} >Börja din sökning</p>
        <button class=" text-red-500 rounded-3xl h-9 self-end w-1/12" onclick={searchDocument}>{searchingEnabled ? 'Sök' : 'Skicka'}</button>
    </div>
    <button class=" rounded-3xl w-1/12 flex flex-row items-center justify-center" onclick={() => searchingEnabled=!searchingEnabled} >
        {#if searchingEnabled}
        <img alt="Search" src="/search.svg" class="w-6 h-6" />
        {:else}
        <img alt="Chat" src="/chat.svg" class="w-6 h-6" />
        {/if}
    </button>
    </div>
    </div>
   
</div>
</div>

