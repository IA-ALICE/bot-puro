document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');
    const chatToggleButton = document.getElementById('chat-toggle-button');
    // const closeChatButton = document.getElementById('close-chat-button'); // Keep this commented if not used in HTML

    // if (closeChatButton) { // Keep this commented if not used in HTML
    //     closeChatButton.addEventListener('click', function() {
    //         chatContainer.classList.remove('visible');
    //         chatContainer.classList.add('hidden');
    //     });
    // }

    // Función para alternar la visibilidad del chat
    chatToggleButton.addEventListener('click', function() {
        if (chatContainer.classList.contains('hidden')) {
            chatContainer.classList.remove('hidden');
            chatContainer.classList.add('visible');
            if (chatMessages.childElementCount === 0) {
                fetch('/api/get_initial_message')
                    .then(response => response.json())
                    .then(data => {
                        addMessage(data.response, 'bot');
                    })
                    .catch(error => {
                        console.error('Error loading initial message:', error);
                        addMessage('Lo siento, no pude cargar el mensaje inicial.', 'bot');
                    });
            } else {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            userInput.focus(); // Enfocar el input al abrir el chat
        } else {
            chatContainer.classList.remove('visible');
            chatContainer.classList.add('hidden');
        }
    });

    // Función para añadir mensajes y procesar formato (negritas, listas)
    function addMessage(text, sender) {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble', sender);

        let processedText = String(text); // Asegurarse de que sea un string

        // Reemplazar saltos de línea por <br>
        processedText = processedText.replace(/\n/g, '<br>');

        // **LÓGICA PARA NEGRITAS CON DOBLE ASTERISCO**
        processedText = processedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Lógica para listas con un solo asterisco y espacio al inicio de línea
        const lines = processedText.split('<br>');
        let finalHtml = '';
        let inList = false;

        lines.forEach(line => {
            const trimmedLine = line.trim();
            if (trimmedLine.startsWith('* ')) {
                if (!inList) {
                    finalHtml += '<ul>';
                    inList = true;
                }
                let listItemContent = trimmedLine.substring(2);
                listItemContent = listItemContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                finalHtml += `<li>${listItemContent}</li>`;
            } else {
                if (inList) {
                    finalHtml += '</ul>';
                    inList = false;
                }
                if (trimmedLine !== '') {
                    let paragraphContent = trimmedLine.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                    finalHtml += `<p>${paragraphContent}</p>`;
                }
            }
        });

        if (inList) {
            finalHtml += '</ul>';
        }

        messageBubble.innerHTML = finalHtml || processedText;

        chatMessages.appendChild(messageBubble);

        userInput.setAttribute('type', 'text');
        userInput.setAttribute('placeholder', 'Escribe tu mensaje...');
        userInput.focus();

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage(message) {
        addMessage(message, 'user');

        userInput.value = '';

        sendButton.disabled = true;
        userInput.disabled = true;

        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot');
            sendButton.disabled = false;
            userInput.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Lo siento, hubo un error al procesar tu solicitud.', 'bot');
            sendButton.disabled = false;
            userInput.disabled = false;
        });
    }

    sendButton.addEventListener('click', function() {
        if (userInput.value.trim() !== '') {
            sendMessage(userInput.value.trim());
        }
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && userInput.value.trim() !== '') {
            sendMessage(userInput.value.trim());
        }
    });
});