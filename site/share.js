for (const controls of document.querySelectorAll(".share-controls")) {
    const button = controls.querySelector("[data-copy-link]");
    const input = controls.querySelector("input");
    const status = controls.querySelector("[role=status]");
    button.hidden = false;

    button.addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(input.value);
            input.hidden = true;
            status.textContent = "Link copied.";
        } catch {
            input.hidden = false;
            input.focus();
            input.select();
            status.textContent = "Copy the selected link.";
        }
    });
}
