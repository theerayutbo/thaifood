document.addEventListener('DOMContentLoaded', function() {
    const aiUserInput = document.getElementById('ai-user-input');
    const aiAskGeneralButton = document.getElementById('ai-ask-general-button');
    const aiGetRecipeButton = document.getElementById('ai-get-recipe-button');
    const aiChatArea = document.getElementById('ai-chat-area');

    // uiTextsJS and currentLocaleJS are passed from layout.html
    // e.g. uiTextsJS.ollamaThinking

    function addMessageToChat(message, sender, isLoading = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'ai-message');
        if (isLoading) {
            messageDiv.classList.add('loading-message'); // For potential styling of loading messages
            messageDiv.innerHTML = `${message} <span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>`;
        } else {
            // Basic Markdown-like formatting for newlines
            messageDiv.innerHTML = message.replace(/\n/g, '<br>');
        }
        aiChatArea.appendChild(messageDiv);
        aiChatArea.scrollTop = aiChatArea.scrollHeight;
        return messageDiv; // Return the message element if we need to update it (e.g. loading message)
    }

    function removeLoadingMessage() {
        const loadingMsg = aiChatArea.querySelector('.loading-message');
        if (loadingMsg) {
            loadingMsg.remove();
        }
    }

    function highlightAndScrollToItem(itemId) {
        const highlightedElements = document.querySelectorAll('.highlighted-item');
        highlightedElements.forEach(el => el.classList.remove('highlighted-item'));

        const itemElement = document.getElementById("menu-item-" + itemId);
        if (itemElement) {
            itemElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            itemElement.classList.add('highlighted-item');
            setTimeout(() => {
                itemElement.classList.remove('highlighted-item');
            }, 3000); // Highlight for 3 seconds
        } else {
            console.warn("Item with ID: menu-item-" + itemId + " not found on this page.");
            const mainContent = document.querySelector('.main-content .item-grid');
            if (!mainContent || !mainContent.querySelector(`#menu-item-${itemId}`)) {
                 addMessageToChat(uiTextsJS.itemNotFoundOnPage, 'ai');
            } else {
                 addMessageToChat(uiTextsJS.itemNotFoundCurrentList, 'ai');
            }
        }
    }

    async function handleAIQuery(mode) {
        const query = aiUserInput.value.trim();
        if (query === "") {
            aiUserInput.placeholder = (mode === 'recipe_suggestion') ? uiTextsJS.recipeInputPlaceholder : uiTextsJS.ollamaError; // A bit of a misuse for empty error
            return;
        }

        addMessageToChat(query, 'user');
        aiUserInput.value = ""; // Clear input
        const loadingMessageElement = addMessageToChat(uiTextsJS.ollamaThinking, 'ai', true);


        try {
            const response = await fetch('/api/ollama/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query, mode: mode }),
            });

            removeLoadingMessage(); // Remove "AI is thinking..."

            if (!response.ok) {
                const errorData = await response.json();
                addMessageToChat(errorData.answer || uiTextsJS.ollamaError, 'ai');
                return;
            }

            const data = await response.json();
            addMessageToChat(data.answer, 'ai');

            if (data.action === "highlight_item" && data.item_id) {
                highlightAndScrollToItem(data.item_id);
            }

        } catch (error) {
            console.error('Error asking AI:', error);
            removeLoadingMessage();
            addMessageToChat(uiTextsJS.ollamaError, 'ai');
        }
    }

    if (aiAskGeneralButton) {
        aiAskGeneralButton.addEventListener('click', () => handleAIQuery('general_query'));
    }
    if (aiGetRecipeButton) {
        aiGetRecipeButton.addEventListener('click', () => handleAIQuery('recipe_suggestion'));
    }

    if (aiUserInput) {
        aiUserInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                // Default to general query if enter is pressed, or decide based on context
                // For simplicity, let's assume 'Enter' triggers general query or requires a primary button
                // Or, perhaps disable 'Enter' and force button clicks for clarity of mode.
                // For now, let's make Enter trigger general query:
                // handleAIQuery('general_query');
                // Better: Don't do anything on enter, force button click for mode.
            }
        });
        aiUserInput.addEventListener('focus', () => {
            aiUserInput.placeholder = currentLocaleJS === 'th' ? ui_texts.th.ai_input_placeholder : ui_texts.en.ai_input_placeholder;
        });
    }

    document.querySelectorAll('.add-to-cart-button').forEach(button => {
        button.addEventListener('click', function() {
            const itemName = this.dataset.itemName; // Get name from data attribute
            const itemId = this.dataset.itemId;

            if (aiChatArea) {
                 let message = uiTextsJS.cartItemAddedResponse.replace('{item_name}', itemName);
                 addMessageToChat(message, 'ai');
                 if(itemId) {
                    highlightAndScrollToItem(itemId);
                 }
            }
        });
    });
});

// CSS for thinking dots (add to your style.css or a new one)
/*
.thinking-dots span {
    animation: blink 1.4s infinite both;
    display: inline-block;
}
.thinking-dots span:nth-child(2) {
    animation-delay: .2s;
}
.thinking-dots span:nth-child(3) {
    animation-delay: .4s;
}
@keyframes blink {
    0% { opacity: .2; }
    20% { opacity: 1; }
    100% { opacity: .2; }
}
*/