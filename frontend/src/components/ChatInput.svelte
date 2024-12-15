<script lang="ts">
    let {fileInput, onFileChange, searchDocument } : {fileInput: HTMLElement | null, onFileChange: (event: Event) => void , searchDocument: (searchString: string, allowSend: boolean) => any} = $props()

    // Message to be sent
    let search = $state('')

    // False if the user is waiting for a response from the AI
    let allowSend = $state(true)

    // True if the user is searching within a document, false if the user is sending a regular chat message
    let searchingEnabled = $state(false)


    // Handle keyboard input, enable using enter key to send message and shift+enter to create a new line
    function onkeyenter(event: KeyboardEvent) {
    console.log(event)
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault()
        if(allowSend && search.trim() !== "") {

           searchDocument(search, allowSend)
           search=""
            
            }

            }
}

// Function to click the file input element
function uploadFile() {
        if(fileInput) {
            fileInput.click()    
        }
    }






</script>


<div class="w-full flex flex-row items-center">
    <input type="file" id="file" name="file" accept=".pdf" class="hidden" bind:this={fileInput}  onchange={onFileChange}/>
    <button class=" text-gray-500 rounded-3xl h-9 w-1/12" onclick={() => uploadFile()} >+</button>
    <div class="border border-gray-300 rounded-3xl px-3 w-full flex flex-row items-center justify-between py-2 ">
        <p id="search" onkeydown={onkeyenter} contenteditable bind:innerText={search} class=" w-10/12 outline-none" ></p>
        <p class={search.length==0 ? ' block absolute -z-10 text-gray-500' : 'hidden'} >Börja din sökning</p>
        <button class="  disabled:text-gray-500 text-red-500 rounded-3xl h-9 self-end w-1/12" disabled={!(allowSend && search.trim() !== '')} onclick={() => {searchDocument(search, allowSend); search=""}}>{searchingEnabled ? 'Sök' : 'Skicka'}</button>
    </div>
    <button class=" rounded-3xl w-1/12 flex flex-row items-center justify-center" onclick={() => searchingEnabled=!searchingEnabled} >
        {#if searchingEnabled}
        <img alt="Search" src="/search.svg" class="w-6 h-6" />
        {:else}
        <img alt="Chat" src="/chat.svg" class="w-6 h-6" />
        {/if}
    </button>
</div>