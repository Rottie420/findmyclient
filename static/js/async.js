const homeInput = document.getElementById("homeQuery");
const chatInputField = document.getElementById("chatQuery");
const chat = document.getElementById("chat");
const home = document.getElementById("home");
const chatInput = document.getElementById("chatInput");


function createActionButtons() {
    return `
        <div class="message-actions">
            <button onclick="copyMessage(this)"><svg><use href="/static/svg/copy.svg"></use></svg></button>
            <button onclick="downloadMessage(this)"><svg><use href="/static/svg/download.svg"></use></svg></button>
        </div>
    `;
}


function copyMessage(button) {
    const text = button.closest(".message").querySelector(".message-content").innerText;

    navigator.clipboard.writeText(text);

    button.innerHTML = `<svg><use href="/static/svg/copy.svg"></use></svg>`;

    setTimeout(() => {
        button.innerHTML = `<svg><use href="/static/svg/copy.svg"></use></svg>`;
    }, 1500);
}


function downloadMessage(button) {

    const message = button.closest(".message");
    const emailElements = message.querySelectorAll(".message-content div");

    let emails = [];

    emailElements.forEach(el => {

        const text = el.innerText.replace("📧", "").trim();

        if (text.includes("@")) {
            emails.push(text);
        }

    });

    const csvContent = "Email\n" + emails.join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });

    const a = document.createElement("a");

    a.href = URL.createObjectURL(blob);
    a.download = "emails.csv";

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(a.href);
}


async function sendMessage(customText = null) {

    const input = home.style.display !== "none"
        ? homeInput
        : chatInputField;

    const text = (customText || input.value).trim();
    if (!text) return;

    home.style.display = "none";
    chat.style.display = "block";
    chatInput.style.display = "block";

    const user = document.createElement("div");
    user.className = "message user";
    user.innerHTML = `<div class="message-content">${text}</div>`;
    chat.appendChild(user);

    input.value = "";

    const id = "loading-" + Date.now();

    const loading = document.createElement("div");
    loading.className = "message assistant";
    loading.id = id;
    loading.innerHTML = `🔍 Searching emails<span class="dots"></span>`;
    chat.appendChild(loading);

    chat.scrollTop = chat.scrollHeight;

    const form = new FormData();
    form.append("query", text);

    try {
        const res = await fetch("/search", {
            method: "POST",
            body: form
        });

        const data = await res.json();
        pollResults(data.job_id, id);

    } catch (err) {
        document.getElementById(id).textContent = "❌ Request failed";
    }
}


async function pollResults(jobId, loadingId) {

    const interval = setInterval(async () => {

        const res = await fetch(`/result/${jobId}`);
        const data = await res.json();

        if (data.status === "completed") {

            clearInterval(interval);

            const r = data.result;

            let emailsHTML = "";

            (r.emails || []).forEach(e => {
                emailsHTML += `<div>📧 ${e}</div>`;
            });

            const resultHTML = `
                <div class="message-content">
                    <b>Results for:</b> ${r.query}<br>
                    Total Emails: <b>${r.total_emails_found}</b>
                    <hr>
                    ${emailsHTML || "No emails found. Try another keyword."}
                </div>
            `;

            document.getElementById(loadingId).outerHTML = `
                <div class="message assistant">
                    ${resultHTML}
                    ${createActionButtons()}
                </div>
            `;

            chat.scrollTop = chat.scrollHeight;
        }

        if (data.status === "failed") {

            clearInterval(interval);

            document.getElementById(loadingId).outerHTML = `
                <div class="message assistant">
                    <div class="message-content">⚠️ Failed</div>
                    ${createActionButtons()}
                </div>
            `;
        }

    }, 2000);
}


function handleEnter(e, value) {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage(value);
    }
}


document.addEventListener("keydown", function (e) {

    if (e.key !== "Enter") return;

    const active = document.activeElement;

    if (!active) return;

    if (active.id === "homeQuery" || active.id === "chatQuery") {

        e.preventDefault();
        sendMessage(active.value);
    }
});