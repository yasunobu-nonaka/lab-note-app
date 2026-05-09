const container = document.getElementById("tag-forms");
const addButton = document.getElementById("add-tag");
const message = document.getElementById("tag-form-error");

addButton.addEventListener("click", function () {
    // タグフォームの数
    const count = container.children.length;

    // タグフォームの数が10個を超えないようにする
    if (count >= 10) {
        message.textContent = "タグは10個まで追加できます。";
        return;
    }

    message.textContent = "";

    const template = document.getElementById("tag-template").innerHTML;
    container.insertAdjacentHTML("beforeend", template);
    reindex();
    rebindRemoveButtons();
});

// フォームの削除機能を付与
function rebindRemoveButtons() {
    document.querySelectorAll(".remove-tag").forEach((button) => {
    button.onclick = function () {
        this.parentElement.remove();
        reindex();
        message.textContent = "";
    };
    });
}

// フォームのidとnameのインデックスを再設定
function reindex() {
    const entries = document.querySelectorAll(".tag-entry");

    entries.forEach((entry, index) => {
        const input = entry.querySelector("input");

        input.name = `tags-${index}-tagname`;
        input.id = `tags-${index}-tagname`;
    });
}

rebindRemoveButtons();