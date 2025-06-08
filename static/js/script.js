document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const optionsContainer = document.getElementById('options-container');
    const chatContainer = document.getElementById('chat-container');
    const chatToggleButton = document.getElementById('chat-toggle-button');

    // Función para alternar la visibilidad del chat
    chatToggleButton.addEventListener('click', function() {
        if (chatContainer.classList.contains('hidden')) {
            chatContainer.classList.remove('hidden');
            chatContainer.classList.add('visible');
            if (chatMessages.childElementCount === 0) {
                fetch('/api/get_initial_message')
                    .then(response => response.json())
                    .then(data => {
                        addMessage(data.response, 'bot', data.options, data.input_type);
                    })
                    .catch(error => {
                        console.error('Error loading initial message:', error);
                        addMessage('Lo siento, no pude cargar el mensaje inicial.', 'bot');
                    });
            } else {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        } else {
            chatContainer.classList.remove('visible');
            chatContainer.classList.add('hidden');
        }
    });

    function addMessage(text, sender, options = [], inputType = 'number') {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble', sender);

        const messageText = typeof text === 'string' ? text : JSON.stringify(text);
        messageBubble.innerHTML = messageText.replace(/\n/g, '<br>');
        chatMessages.appendChild(messageBubble);

        optionsContainer.innerHTML = ''; // Limpiar opciones anteriores

        if (options && options.length > 0) {
            // Variable para la enumeración secuencial, excluyendo la opción "Volver" si es 0
            let displayIndex = 1;
            options.forEach(option => {
                if (option.id !== "restart") { // Asegúrate de que "restart" no se muestre
                    const button = document.createElement('button');
                    button.classList.add('option-button');

                    // APLICA LA NUMERACIÓN SECUENCIAL PARA LAS OPCIONES QUE NO SEAN "0. Volver..."
                    if (option.id === 0 || String(option.id).toLowerCase() === '0') {
                        button.textContent = "0. Volver a la lista de " + (
                            // Intenta deducir el contexto del "Volver"
                            text.includes("APARTADOS DEL CATÁLOGO") ? "Servicios Principales" :
                            text.includes("PREGUNTAS PARA") ? "Apartados del Catálogo" :
                            text.includes("RESPUESTAS PARA") ? "Preguntas" :
                            text.includes("lista de promociones") ? "promociones" : // Este caso ya no debería ocurrir así pero se deja como ejemplo
                            text.includes("lista de categorías") ? "categorías" : // Este caso ya no debería ocurrir así pero se deja como ejemplo
                            "opciones anteriores"
                        );
                        button.dataset.id = 0; // El ID real sigue siendo 0 para el backend
                    } else {
                        // Usa displayIndex para la numeración visible
                        button.textContent = `${displayIndex}. ${option.text.split('. ').slice(1).join('. ') || option.text}`;
                        button.dataset.id = option.id; // Envía el ID real al backend
                        displayIndex++; // Incrementa para la siguiente opción
                    }

                    button.addEventListener('click', function() {
                        sendMessage(button.dataset.id);
                    });
                    optionsContainer.appendChild(button);
                }
            });
        }

        if (inputType === 'number') {
            userInput.setAttribute('type', 'number');
            userInput.setAttribute('placeholder', 'Escribe tu número de opción...');
        } else {
            userInput.setAttribute('type', 'text');
            userInput.setAttribute('placeholder', 'Escribe tu mensaje...');
        }
        userInput.focus();

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage(message) {
        addMessage(message, 'user');

        userInput.value = '';

        sendButton.disabled = true;
        userInput.disabled = true;
        Array.from(optionsContainer.children).forEach(button => button.disabled = true);

        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot', data.options, data.input_type);
            sendButton.disabled = false;
            userInput.disabled = false;
            Array.from(optionsContainer.children).forEach(button => button.disabled = false);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Lo siento, hubo un error al procesar tu solicitud.', 'bot');
            sendButton.disabled = false;
            userInput.disabled = false;
            Array.from(optionsContainer.children).forEach(button => button.disabled = false);
        });
    }

    sendButton.addEventListener('click', function() {
        if (userInput.value.trim() !== '') {
            sendMessage(userInput.value);
        }
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && userInput.value.trim() !== '') {
            sendMessage(userInput.value);
        }
    });
});