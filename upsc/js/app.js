// =====================================================
// Globals
// =====================================================

let notes = [];
let selectedNote = null;

// =====================================================
// Build Folder Tree
// =====================================================

function buildTree(notes) {

    const tree = {};

    notes.forEach(note => {

        const folders = note.folder.split("/");

        let current = tree;

        folders.forEach(folder => {

            if (!current[folder]) {

                current[folder] = {};

            }

            current = current[folder];

        });

        if (!current.__files__) {

            current.__files__ = [];

        }

        current.__files__.push(note);

    });

    return tree;

}

// =====================================================
// Render Folder Tree
// =====================================================

function renderTree(node) {

    let html = "";

    Object.keys(node)
        .filter(key => key !== "__files__")
        .sort()
        .forEach(folder => {

            html += `

<div class="folder">

    <div class="folder-name">

        📂 ${folder}

    </div>

    ${renderTree(node[folder])}

</div>

`;

        });

    if (node.__files__) {

        node.__files__.forEach(note => {

            html += `

<div
    class="note"
    data-file="${note.path}"
    onclick="loadMarkdown('${note.path}')">

    📄 ${note.title}

</div>

`;

        });

    }

    return html;

}

// =====================================================
// Highlight Selected Note
// =====================================================

function highlightSelected(file){

    document
        .querySelectorAll(".note")
        .forEach(note=>{

            note.classList.remove("active");

        });

    const current =
        document.querySelector(
            `[data-file="${CSS.escape(file)}"]`
        );

    if(current){

        current.classList.add("active");

    }

}

// =====================================================
// Update Header
// =====================================================

function updateHeader(file){

    const title =
        file
            .split("/")
            .pop()
            .replace(".md","");

    document.getElementById("doc-title").innerText =
        "";

    document.getElementById("breadcrumb").innerText =
        file
            .replace("notes/","")
            .replace(".md","")
            .replaceAll("/","  >  ");

}

// =====================================================
// Convert Custom Blocks
// =====================================================

function processCustomBlocks() {

    document
        .querySelectorAll("pre code.language-mindmap")
        .forEach(code => {

            const div = document.createElement("div");

            div.className = "mindmap";

            div.textContent = code.textContent;

            code.parentElement.replaceWith(div);

        });

}

// =====================================================
// Load Markdown
// =====================================================

async function loadMarkdown(file) {

    selectedNote = file;

    history.replaceState(
        {},
        "",
        "?file=" + encodeURIComponent(file)
    );

    highlightSelected(file);

    updateHeader(file);

    const response = await fetch(file);

    const markdown = await response.text();

    document.getElementById("content").innerHTML =
        marked.parse(markdown);

    processCustomBlocks();

    window.scrollTo({
        top:0,
        behavior:"smooth"
    });

}

// =====================================================
// Load Notes
// =====================================================

async function loadNotes() {

    const response =
        await fetch("data/notes.json");

    notes =
        await response.json();

    const tree =
        buildTree(notes);

    document.getElementById("tree").innerHTML =
        renderTree(tree);

    const params =
        new URLSearchParams(window.location.search);

    const file =
        params.get("file");

    if(file){

        loadMarkdown(file);

    }

}

// =====================================================
// Start
// =====================================================

loadNotes();