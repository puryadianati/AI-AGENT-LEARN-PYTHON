const challengeAssist = (question) => {
    // Store challenge type in localStorage
    localStorage.setItem('challenge', question.type);

    // Clear the mid-row section
    document.querySelector('.mid-row').innerHTML = '';
    console.log(question);

    // Create the challenge assist container
    let challengeAssistDiv = document.createElement("div");
    challengeAssistDiv.className = "challenge-assist";

    // Create the assist section
    let assistSectionDiv = document.createElement("div");
    assistSectionDiv.className = "challenge-section";

    // Create the assist header
    let assistHeaderDiv = document.createElement("div");
    assistHeaderDiv.className = "challenge-header";

    // Create and append the header text
    let h1Element = document.createElement("h1");
    let spanElement = document.createElement("span");
    spanElement.innerText = "Select the correct meaning";
    h1Element.appendChild(spanElement);

    // Create the assist content container
    let assistContentDiv = document.createElement("div");
    assistContentDiv.className = "assist-content";

    // Create the question section
    let assistContentQuestionDiv = document.createElement("div");
    assistContentQuestionDiv.className = "assist-content-question";

    // Create the question row
    let assistQuestionRowDiv = document.createElement("div");
    assistQuestionRowDiv.className = "assist-question-row";

    // Create the character animation container
    let assistCharacterDiv = document.createElement("div");
    assistCharacterDiv.id = "assist-character";

    // Create the word container
    let assistWordContainerDiv = document.createElement("div");
    assistWordContainerDiv.className = "assist-word-container";

    // Create the text container
    let containerDiv = document.createElement("div");

    // Create the question text
    let assistTextDiv = document.createElement("div");
    assistTextDiv.id = "assist-text";

    // Create the projection container
    let containerProjectionDiv = document.createElement("div");
    containerProjectionDiv.className = "container-projection";

    // Create the projection
    let projectionDiv = document.createElement("div");
    projectionDiv.className = "projection";

    // Create the options container
    let assistContentOptionsDiv = document.createElement("div");
    assistContentOptionsDiv.id = "assist-content-options";

    // Append elements to their parents
    containerDiv.appendChild(assistTextDiv);
    containerProjectionDiv.appendChild(projectionDiv);
    assistWordContainerDiv.appendChild(containerDiv);
    assistWordContainerDiv.appendChild(containerProjectionDiv);
    assistQuestionRowDiv.appendChild(assistCharacterDiv);
    assistQuestionRowDiv.appendChild(assistWordContainerDiv);
    assistContentQuestionDiv.appendChild(assistQuestionRowDiv);
    assistContentDiv.appendChild(assistContentQuestionDiv);
    assistContentDiv.appendChild(assistContentOptionsDiv);

    assistHeaderDiv.appendChild(h1Element);
    assistHeaderDiv.appendChild(assistContentDiv);
    assistSectionDiv.appendChild(assistHeaderDiv);
    challengeAssistDiv.appendChild(assistSectionDiv);

    // Append the challenge assist container to the mid-row section
    let midRowDiv = document.querySelector('.mid-row');
    midRowDiv.appendChild(challengeAssistDiv);

    // Load the animation using the static path
    let animationPath = "{% static 'zaban/assets/json-animations/assistheader.json' %}";
    const animation = bodymovin.loadAnimation({
        container: document.getElementById('assist-character'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: animationPath
    });

    // Set the question prompt
    document.getElementById('assist-text').textContent = question.prompt;
    const choices = question.options;

    // Store the correct answer in localStorage
    localStorage.setItem('correctIndex', question.correctIndex + 1);
    localStorage.setItem('solution', question.choices[question.correctIndex]);

    // Create and append the options
    const assistContent = document.getElementById('assist-content-options');
    let outerOptionsCounter = 1;
    let optionCounter = 1;
    choices.forEach(choice => {
        const outerOptionsDiv = document.createElement("div");
        outerOptionsDiv.className = "outer-options-div";
        outerOptionsDiv.id = "outer-options-div-" + optionCounter;

        // Create audio element for the choice
        const audio = new Audio(choice.tts);

        // Create the option button
        const optionDiv = document.createElement("div");
        optionDiv.className = "option-div";
        optionDiv.id = optionCounter.toString();
        optionDiv.addEventListener("click", function () {
            selectOptionButton(this.id);
            buttonClickAnimation(this.id);
            audio.play();
        });

        // Create the option number
        const optionNoSpan = document.createElement("span");
        optionNoSpan.className = "option-no";
        optionNoSpan.id = "option-no-" + optionCounter;
        optionNoSpan.textContent = optionCounter;

        // Create the option text
        const optionNameSpan = document.createElement("span");
        optionNameSpan.className = "option-name";
        optionNameSpan.id = "option-name-" + optionCounter;
        optionNameSpan.textContent = choice.text;

        // Append the option number and text to the button
        optionDiv.appendChild(optionNoSpan);
        optionDiv.appendChild(optionNameSpan);

        // Append the button to the outer options container
        outerOptionsDiv.appendChild(optionDiv);

        // Append the outer options container to the assist content
        assistContent.appendChild(outerOptionsDiv);

        // Increment counters for unique IDs
        outerOptionsCounter++;
        optionCounter++;
    });
};
