
(function () {
    "use strict";

    const selectors = {
        self: '[data-cmp-is="qualtrics"]',
        like: '[data-cmp-hook-qualtrics="like"]',
        disLike: '[data-cmp-hook-qualtrics="dis-like"]',
    };

    const classes = {
        qualtrics: '.cmp-qualtrics',
        feedbackOne: '.cmp-qualtrics__feedback-one',
        feedbackTwo: '.cmp-qualtrics__feedback-two',
        feedbackThree: '.cmp-qualtrics__feedback-three',
        rating: '.cmp-qualtrics__rating',
        feedback: '.cmp-qualtrics__feedback',
        qualtricsText: '.cmp-qualtrics__text',
        close: '.cmp-qualtrics__close',
    };

    function closeSurvey(event) {
        event.preventDefault();
        document.querySelector(classes.qualtrics).style.display = "none";
    }

    function submit(event) {
        event.preventDefault();
        const sessionId = document.querySelector(classes.feedbackOne).getAttribute("sessionId");
        const questionId = document.querySelector(classes.feedback).getAttribute("questionId");
        const surveyId = document.querySelector(classes.qualtrics).getAttribute("survey-id");
        const input = document.querySelector(classes.qualtricsText).value;
        var params = 'surveyId=' + surveyId + '&sessionId=' + sessionId + '&questionId=' + questionId + "&input=" + input + "&step=Three";
        var requestThree = new XMLHttpRequest();
        requestThree.open("GET", "/bin/akamai/qualtrics?" + params);
        requestThree.onreadystatechange = function () {
            if ((requestThree.readyState === 4) && (requestThree.status === 200)) {
                var data = JSON.parse(requestThree.responseText);
                if (data && data.result) {
                    const feedbackThree = document.createElement("div");
                    feedbackThree.classList.add("cmp-feedback", "cmp-qualtrics__feedback-three");
                    feedbackThree.setAttribute("data-cmp-hook-qualtrics", "cmp-qualtrics__feedback-three");
                    const textAraea = document.createElement("div");
                    textAraea.classList.add("cmp-qualtrics__textarea");
                    const text = document.createElement("p");
                    const thanksElemment = document.createElement("div");
                    thanksElemment.innerHTML = data.result.done;
                    const thankyouMessage = thanksElemment.innerText;
                    text.innerText = thankyouMessage;
                    textAraea.appendChild(text);
                    const label = document.createElement("label");
                    label.classList.add("cmp-qualtrics__close");
                    label.innerText = "Close Button";
                    label.setAttribute("data-cmp-hook-qualtrics", "close");
                    label.addEventListener("click", closeSurvey);
                    feedbackThree.appendChild(textAraea);
                    feedbackThree.appendChild(label);
                    document.querySelector(classes.feedbackTwo).style.display = "none";
                    document.querySelector(classes.qualtrics).appendChild(feedbackThree);
                } else {
                    document.querySelector(classes.qualtrics).style.display = "none";
                }
            }
        };
        requestThree.send();
    }

    function likeOrDislike(event) {
        event.preventDefault();
        const sessionId = document.querySelector(classes.feedbackOne).getAttribute("sessionId");
        const questionId = document.querySelector(classes.rating).getAttribute("questionId");
        const choiceId = event.target.getAttribute("choiceId");
        const surveyId = document.querySelector(classes.qualtrics).getAttribute("survey-id");
        var params = 'surveyId=' + surveyId + '&sessionId=' + sessionId + '&questionId=' + questionId + '&choiceId=' + choiceId + "&step=Two";
        var requesttwo = new XMLHttpRequest();
        requesttwo.open("GET",
            "/bin/akamai/qualtrics?" + params);
        requesttwo.onreadystatechange = function () {
            if ((requesttwo.readyState === 4) && (requesttwo.status === 200)) {
                var data = JSON.parse(requesttwo.responseText);
                if (data && data.result) {
                    const feedbackTwo = document.createElement("div");
                    feedbackTwo.classList.add("cmp-feedback", "cmp-qualtrics__feedback-two");
                    feedbackTwo.setAttribute("data-cmp-hook-qualtrics", "cmp-qualtrics__feedback-two");
                    const textAraea = document.createElement("div");
                    textAraea.classList.add("cmp-qualtrics__textarea");
                    const text = document.createElement("p");
                    text.innerText = data.result.questions[0].display;
                    textAraea.appendChild(text);
                    const feedback = document.createElement("div");
                    feedback.classList.add("cmp-qualtrics__feedback");
                    feedback.setAttribute("questionId", data.result.questions[0].questionId);
                    const input = document.createElement("input");
                    input.classList.add("cmp-qualtrics__text");
                    input.setAttribute("type", "text");
                    input.setAttribute("placeholder", document.querySelector(classes.qualtrics).getAttribute("placeholder-text"));
                    const submitButtonText = document.querySelector(classes.qualtrics).getAttribute("submit-text");
                    const button = document.createElement("button");
                    button.classList.add("cmp-qualtrics-button");
                    button.setAttribute("target", "_self");
                    button.setAttribute("aria-label", submitButtonText);
                    button.addEventListener("click", submit);
                    const span = document.createElement("span");
                    span.classList.add("cmp-button__text");
                    span.innerText = submitButtonText;
                    button.appendChild(span);
                    feedback.appendChild(input);
                    feedback.appendChild(button);
                    const label = document.createElement("label");
                    label.classList.add("cmp-qualtrics__close");
                    label.innerText = "Close Button";
                    label.setAttribute("data-cmp-hook-qualtrics", "close");
                    label.addEventListener("click", closeSurvey);
                    feedbackTwo.appendChild(textAraea);
                    feedbackTwo.appendChild(feedback);
                    feedbackTwo.appendChild(label);
                    document.querySelector(classes.qualtrics).appendChild(feedbackTwo);
                    document.querySelector(classes.feedbackOne).style.display = "none";
                } else {
                    document.querySelector(classes.qualtrics).style.display = "none";
                }
            }
        };
        requesttwo.send();
    }

    function Qualtrics(config) {
        function init() {
            config.element.removeAttribute("data-cmp-is");
        }

        if (config && config.element) {
            init();
        }
    }

    var isSurveyDisplayed = false;

    function initQualtricsSurvey(){
        if (document.querySelector(classes.qualtrics) && !isSurveyDisplayed) {
            var request = new XMLHttpRequest();
            const surveyId = document.querySelector(classes.qualtrics).getAttribute("survey-id");
            const language = document.querySelector(classes.qualtrics).getAttribute("language");
            const qualtrics = document.querySelector(classes.qualtrics);
            const pageUrl = document.location.href;
            request.open(
                'GET',
                '/bin/akamai/qualtrics?surveyId=' + surveyId + '&language=' + language + "&step=One"+ "&pageUrl=" + pageUrl);
            request.onreadystatechange = function () {
                if ((request.readyState === 4) && (request.status === 200)) {
                    var data = JSON.parse(request.responseText);
                    if (data && data.result) {
                        const feedbackOne = document.createElement("div");
                        feedbackOne.classList.add("cmp-feedback", "cmp-qualtrics__feedback-one");
                        feedbackOne.setAttribute("data-cmp-hook-qualtrics", "cmp-qualtrics__feedback-one");
                        feedbackOne.setAttribute("sessionId", data.result.sessionId);
                        const textArea = document.createElement("div");
                        textArea.classList.add("cmp-qualtrics__textarea");
                        const text = document.createElement("p");
                        text.innerText = data.result.questions[0].display;
                        textArea.appendChild(text);
                        const rating = document.createElement("div");
                        rating.classList.add("cmp-qualtrics__rating");
                        rating.setAttribute("questionId", data.result.questions[0].questionId);
                        const like = document.createElement("div");
                        like.classList.add("cmp-qualtrics__like");
                        like.setAttribute("data-cmp-hook-qualtrics", "like");
                        like.setAttribute("choiceId", data.result.questions[0].choices[0].choiceId);
                        like.addEventListener("click", likeOrDislike);
                        const disLike = document.createElement("div");
                        disLike.classList.add("cmp-qualtrics__dislike");
                        disLike.setAttribute("data-cmp-hook-qualtrics", "dis-like");
                        disLike.setAttribute("choiceId", data.result.questions[0].choices[1].choiceId);
                        disLike.addEventListener("click", likeOrDislike);
                        rating.appendChild(like);
                        rating.appendChild(disLike);
                        feedbackOne.appendChild(textArea);
                        feedbackOne.appendChild(rating);
                        qualtrics.appendChild(feedbackOne);
                        document.querySelector(classes.qualtrics).style.display = "flex";
                        isSurveyDisplayed = true;
                    } else {
                        document.querySelector(classes.qualtrics).style.display = "none";
                    }
                }
            };
            request.send();
        }else{
           if( document.querySelector(classes.qualtrics)){
                document.querySelector(classes.qualtrics).style.display = "none";
           }
        }
    }

    function getValue(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    function checkCookie() {
        var cookieCheck = getValue("OptanonConsent");
        let hideQualtrics = false;
        if (cookieCheck) {
            if (cookieCheck.indexOf("C0003%3A1") > 0) {
                    initQualtricsSurvey();
            }else{
                hideQualtrics = true;
            }
        }else{
            hideQualtrics = true;
        }
        if(hideQualtrics){
            if(document.querySelector(classes.qualtrics)){
                document.querySelector(classes.qualtrics).style.display = 'none';
            }
        }
    }

    function onDocumentReady() {
        var elements = document.querySelectorAll(selectors.self);
        checkCookie();
        for (var i = 0; i < elements.length; i++) {
            new Qualtrics({ element: elements[i] });
        }

        var MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
        var body = document.querySelector("body");
        var observer = new MutationObserver(function (mutations) {
            mutations.forEach(function (mutation) {
                // needed for IE
                var nodesArray = [].slice.call(mutation.addedNodes);
                if (nodesArray.length > 0) {
                    nodesArray.forEach(function (addedNode) {
                        if (addedNode.querySelectorAll) {
                            var elementsArray = [].slice.call(addedNode.querySelectorAll(selectors.self));
                            elementsArray.forEach(function (element) {
                                new Qualtrics({ element: element });
                            });
                        }
                    });
                }
            });
        });

        observer.observe(body, {
            subtree: true,
            childList: true,
            characterData: true
        });
    }

    window.addEventListener('oneTrustCookieAccepted', function() {
        checkCookie();
    }, false);


    if (document.readyState !== "loading") {
        onDocumentReady();
    } else {
        document.addEventListener("DOMContentLoaded", onDocumentReady);
    }
}());