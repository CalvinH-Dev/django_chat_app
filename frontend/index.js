const container = document.getElementById("container");
const template = document.getElementById("item-template");
const form = document.getElementById("form");

form.addEventListener("submit", (event) => {
	event.preventDefault();

	const nameInputRef = document.getElementById("nameInput");
	const messageInputRef = document.getElementById("messageInput");

	const data = { name: nameInputRef.value, message: messageInputRef.value };

	post_message(data);
});

async function fetch_messages() {
	container.innerHTML = "";
	const response = await fetch("http://localhost:8000");
	const data = await response.json();

	for (const message of data) {
		const item = template.content.cloneNode(true);
		const nameSpanRef = item.querySelector(".name");
		const messageSpanRef = item.querySelector(".message");

		nameSpanRef.textContent = message.name;
		messageSpanRef.textContent = message.message;
		container.appendChild(item);
	}
}

async function post_message(data) {
	const response = await fetch("http://localhost:8000", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
	});

	await fetch_messages();
}

fetch_messages();
