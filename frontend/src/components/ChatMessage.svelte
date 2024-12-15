<script module>
    export interface Message {
        text: string,
        sentBy: "user"|"ai"|"info",
        sentAt: Date,
        file?: any
    }
</script>


<script lang="ts">
    import { marked } from 'marked'
    let { message }: { message: Message } = $props()


</script>


<div class={`flex flex-col   my-1 ${message.sentBy === "user" ? 'self-end items-end ' : message.sentBy === 'info' ? 'self-center items-center' :  'self-start items-start '}`}>
    <p class="text-gray-500 text-sm">{message.sentAt.toLocaleTimeString([],{timeStyle: "short"})}</p>
<div class={`rounded-3xl px-3 flex flex-row items-center justify-between py-2  ${message.sentBy === "user" ? ' bg-red-500 text-white' : message.sentBy === "info" ? 'text-sm text-gray-500' :  'bg-white-300 border border-black text-black'}`}>
    {#if message.file}
    <p class="">
        {message.text}
        <a href={URL.createObjectURL(message.file)} download={message.file.name} class=" underline">View </a>
    </p>
    {:else}
    <span class={`prose ${message.sentBy === "user" ? '  text-white' : message.sentBy === "info" ? 'text-sm text-gray-500' :  '  text-black'}`}>
        {@html marked(message.text)}
    </span>
    {/if}
</div>
</div>