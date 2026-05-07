let content_md;
let preview;

let isSyncingEditor = false;
let isSyncingPreview = false;

// ===== marked 設定 =====
marked.setOptions({
    breaks: true,
    headerIds: false,
    mangle: false,
});

// ===== 数式レンダリング =====
function renderMath() {
    if (typeof renderMathInElement === "undefined") return;

    renderMathInElement(preview, {
    delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
    ],
    throwOnError: false,
    });
}

// ===== プレビュー更新 =====
function updatePreview() {
    const markdown = content_md.value;

    const dirtyHtml = marked.parse(markdown);
    const cleanHtml = DOMPurify.sanitize(dirtyHtml);

    preview.innerHTML = cleanHtml;
    renderMath();
}

function syncEditorToPreview() {
    if (isSyncingPreview) return;

    isSyncingEditor = true;

    const editorMax = content_md.scrollHeight - content_md.clientHeight;
    const previewMax = preview.scrollHeight - preview.clientHeight;

    if (editorMax > 0 && previewMax > 0) {
    const ratio = content_md.scrollTop / editorMax;
    preview.scrollTop = ratio * previewMax;
    }

    isSyncingEditor = false;
}

function syncPreviewToEditor() {
    if (isSyncingEditor) return;

    isSyncingPreview = true;

    const editorMax = content_md.scrollHeight - content_md.clientHeight;
    const previewMax = preview.scrollHeight - preview.clientHeight;

    if (editorMax > 0 && previewMax > 0) {
    const ratio = preview.scrollTop / previewMax;
    content_md.scrollTop = ratio * editorMax;
    }

    isSyncingPreview = false;
}

// ===== DOM & KaTeX が揃ってから初期化 =====
document.addEventListener("DOMContentLoaded", () => {
    content_md = document.getElementById("content_md");
    preview = document.getElementById("preview");

    content_md.addEventListener("input", updatePreview);
    content_md.addEventListener("scroll", syncEditorToPreview);
    preview.addEventListener("scroll", syncPreviewToEditor);

    // 初期レンダリング
    updatePreview();
});