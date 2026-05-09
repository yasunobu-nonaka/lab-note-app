document.querySelectorAll('.note-card').forEach(note => {
    const tagList = note.querySelector('.tag-list');
    const tags = [...tagList.querySelectorAll('.tag-item')];
    const badge = tagList.querySelector('.badge');
    const noteBottom = note.getBoundingClientRect().bottom;

    let hiddenCount = 0;

    // ノートの下端からはみ出すタグを非表示にする
    tags.forEach(tag => {
        if (tag.getBoundingClientRect().bottom > noteBottom) {
            tag.classList.add('hidden');
            hiddenCount++;
        }
    });

    // 非表示タグ数をタグの下部に表示する
    if (hiddenCount > 0) {
        badge.textContent = `他${hiddenCount}タグ`;
        badge.classList.remove('hidden');

        // 非表示タグ数がノートの下部からはみ出ス場合は最後のタグを隠す　
        while (badge.getBoundingClientRect().bottom > noteBottom) {
            const visibleTags = tags.filter(t => !t.classList.contains('hidden'));
            if (visibleTags.length === 0) break;

            const lastVisibleTag = visibleTags[visibleTags.length - 1];
            lastVisibleTag.classList.add('hidden');
            hiddenCount++;
            badge.textContent = `他${hiddenCount}タグ`;
        }
    }
})