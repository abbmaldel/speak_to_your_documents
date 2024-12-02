
<script lang='ts'>
    import { io } from "socket.io-client";


    const socket_url = "http://localhost:3000"; // does not work at the moment, needs to be changed to the server's url
    const socket = io(socket_url);
    let search = $state('')
    let allowSend = $state(true)
    let lastElement = $state<null|HTMLElement>(null)
    let fileInput = $state<null|HTMLInputElement>(null)

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

    function onFileChange(event: Event) {
        const file = (event.target as HTMLInputElement).files?.[0]
        if(file) {
            messageList.push({text: `Uploaded ${file.name}`, sentBy: "info", sentAt: new Date(), file: file})
        }
    }   

    function searchDocument() {
        socket.emit('send_message', search, false);
        messageList.push({text: search, sentBy: "user", sentAt: new Date()})
        search = ''
        allowSend = false
        setTimeout(() => {
                messageList.push({text: 'Jag är din AI!', sentBy: "ai", sentAt: new Date()})
                allowSend = true
            }, 1000)
    }
   
    socket.on("new_message", ({answer}) => {
        messageList.push({text: answer, sentBy: "ai", sentAt: new Date()})
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
        <div class={`rounded-3xl px-3 flex flex-row items-center justify-between py-2  ${message.sentBy === "user" ? ' bg-red-500 text-white' : message.sentBy === "info" ? 'text-sm text-gray-500' :  'bg-white-300 border border-black text-black'}`}>
            {#if message.file}
            <p>
                {message.text}
                <a href={URL.createObjectURL(message.file)} download={message.file.name} class=" underline">View </a>
            </p>            
            {:else}
            <p>{message.text}</p>
            {/if}
        </div>
        </div>
        {:else}
        <div class={`flex flex-col   my-1 ${message.sentBy === "user" ? 'self-end items-end ' : message.sentBy === 'info' ? 'self-center items-center' :  'self-start items-start '}`}>
            <p class="text-gray-500 text-sm">{message.sentAt.toLocaleTimeString([],{timeStyle: "short"})}</p>
        <div class={`rounded-3xl px-3 flex flex-row items-center justify-between py-2  ${message.sentBy === "user" ? ' bg-red-500 text-white' : message.sentBy === "info" ? 'text-sm text-gray-500' :  'bg-white-300 border border-black text-black'}`}>
            {#if message.file}
            <p>
                {message.text}
                <a href={URL.createObjectURL(message.file)} download={message.file.name} class=" underline">View </a>
            </p>
            {:else}
            <p>{message.text}</p>
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
        <button class=" text-red-500 rounded-3xl h-9 self-end w-1/12" onclick={searchDocument}>Sök</button>
    </div>
    </div>
    </div>
   
</div>
</div>

