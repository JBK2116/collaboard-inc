/**
 * Create Meeting Form Handler
 * Handles dynamic question management, validation, and form submission
 */

// Configuration
const CONFIG = {
    MAX_QUESTIONS: 50,
    MAX_TITLE_LENGTH: 200,
    MAX_DESCRIPTION_LENGTH: 1000,
    MAX_QUESTION_LENGTH: 300,
    MIN_DURATION: 1,
    MAX_DURATION: 60,
    NOTIFICATION_DURATION: 4000,
};

// State
let questionCount = 1;

/**
 * Initialize the form when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function () {
    initializeCharCounters();
    initializeEventListeners();
    initializeQuestionCounters();
});

/**
 * Initialize character counters for all inputs
 */
function initializeCharCounters() {
    setupCharCounter(
        document.getElementById('title'),
        document.getElementById('titleCount'),
        CONFIG.MAX_TITLE_LENGTH,
    );

    setupCharCounter(
        document.getElementById('description'),
        document.getElementById('descriptionCount'),
        CONFIG.MAX_DESCRIPTION_LENGTH,
    );
}

/**
 * Initialize question character counters
 */
function initializeQuestionCounters() {
    const questions = document.querySelectorAll('.question-input');
    questions.forEach((textarea) => {
        const charCount = textarea
            .closest('.form-group')
            .querySelector('.char-count');
        setupCharCounter(textarea, charCount, CONFIG.MAX_QUESTION_LENGTH);
    });
}

/**
 * Setup character counter for an input element
 */
function setupCharCounter(inputElement, countElement, maxLength) {
    const updateCounter = () => {
        const length = inputElement.value.length;
        countElement.textContent = `${length}/${maxLength}`;

        countElement.classList.remove('warning', 'danger');

        if (length > maxLength * 0.9) {
            countElement.classList.add('danger');
        } else if (length > maxLength * 0.75) {
            countElement.classList.add('warning');
        }
    };

    inputElement.addEventListener('input', updateCounter);
    updateCounter();
}

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // Add question button
    document
        .getElementById('addQuestionBtn')
        .addEventListener('click', addQuestion);

    // Form submission
    document
        .getElementById('createMeetingForm')
        .addEventListener('submit', handleFormSubmit);

    // Real-time validation
    document.getElementById('title').addEventListener('input', function () {
        validateField(this, validateTitle);
    });

    document
        .getElementById('description')
        .addEventListener('input', function () {
            validateField(this, validateDescription);
        });

    document.getElementById('duration').addEventListener('input', function () {
        validateField(this, validateDuration);
    });

    // Question validation (delegated)
    document.addEventListener('input', function (e) {
        if (e.target.classList.contains('question-input')) {
            validateField(e.target, validateQuestion);
        }
    });
}

/**
 * Add a new question to the form
 */
function addQuestion() {
    if (questionCount >= CONFIG.MAX_QUESTIONS) {
        showNotification(
            `You can only add up to ${CONFIG.MAX_QUESTIONS} questions`,
            'error',
        );
        return;
    }

    const container = document.getElementById('questionsContainer');
    const questionItem = createQuestionElement(questionCount);

    container.appendChild(questionItem);

    // Setup character counter for new textarea
    const textarea = questionItem.querySelector('textarea');
    const charCount = questionItem.querySelector('.char-count');
    setupCharCounter(textarea, charCount, CONFIG.MAX_QUESTION_LENGTH);

    questionCount++;
    updateQuestionNumbers();
}

/**
 * Create a new question DOM element
 */
function createQuestionElement(index) {
    const div = document.createElement('div');
    div.className = 'question-item';
    div.setAttribute('data-question-index', index);

    div.innerHTML = `
        <div class="question-header">
            <span class="question-number">Question ${index + 1}</span>
            <button type="button" class="btn-remove-question" onclick="removeQuestion(this)">×</button>
        </div>
        <div class="form-group">
            <textarea 
                name="questions[${index}]" 
                class="form-textarea question-input" 
                maxlength="${CONFIG.MAX_QUESTION_LENGTH}" 
                rows="2" 
                placeholder="Enter your question..." 
                required
                autocomplete="off"
            ></textarea>
            <div class="char-count">0/${CONFIG.MAX_QUESTION_LENGTH}</div>
            <div class="error-message"></div>
        </div>
    `;

    return div;
}

/**
 * Remove a question from the form
 */
window.removeQuestion = function (button) {
    const questionItem = button.closest('.question-item');
    questionItem.remove();
    questionCount--;
    updateQuestionNumbers();
};

/**
 * Update question numbers after add/remove
 */
function updateQuestionNumbers() {
    const questions = document.querySelectorAll('.question-item');

    questions.forEach((item, index) => {
        item.setAttribute('data-question-index', index);
        item.querySelector('.question-number').textContent =
            `Question ${index + 1}`;
        item.querySelector('textarea').name = `questions[${index}]`;

        // Remove delete button from first question
        const deleteBtn = item.querySelector('.btn-remove-question');
        if (index === 0 && deleteBtn) {
            deleteBtn.remove();
        }
    });
}

/**
 * Validation Functions
 */
function validateTitle(value) {
    if (!value || value.trim().length === 0) {
        return 'Meeting title is required';
    }
    if (value.length > CONFIG.MAX_TITLE_LENGTH) {
        return `Title must be ${CONFIG.MAX_TITLE_LENGTH} characters or less`;
    }
    return null;
}

function validateDescription(value) {
    if (value && value.length > CONFIG.MAX_DESCRIPTION_LENGTH) {
        return `Description must be ${CONFIG.MAX_DESCRIPTION_LENGTH} characters or less`;
    }
    return null;
}

function validateDuration(value) {
    const num = parseInt(value);
    if (isNaN(num)) {
        return 'Duration must be a number';
    }
    if (num < CONFIG.MIN_DURATION || num > CONFIG.MAX_DURATION) {
        return `Duration must be between ${CONFIG.MIN_DURATION} and ${CONFIG.MAX_DURATION} minutes`;
    }
    return null;
}

function validateQuestion(value) {
    if (!value || value.trim().length === 0) {
        return 'Question text is required';
    }
    if (value.length > CONFIG.MAX_QUESTION_LENGTH) {
        return `Question must be ${CONFIG.MAX_QUESTION_LENGTH} characters or less`;
    }
    return null;
}

/**
 * Validate a single field
 */
function validateField(inputElement, validatorFn) {
    const error = validatorFn(inputElement.value);

    if (error) {
        showErrorMessage(inputElement, error);
    } else {
        clearErrorMessage(inputElement);
    }
}

/**
 * Show error message for an input
 */
function showErrorMessage(inputElement, message) {
    inputElement.classList.add('error');
    const errorElement = inputElement
        .closest('.form-group')
        .querySelector('.error-message');

    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

/**
 * Clear error message for an input
 */
function clearErrorMessage(inputElement) {
    inputElement.classList.remove('error');
    const errorElement = inputElement
        .closest('.form-group')
        .querySelector('.error-message');

    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

/**
 * Clear all error messages
 */
function clearAllErrors() {
    document
        .querySelectorAll('.error')
        .forEach((el) => el.classList.remove('error'));
    document.querySelectorAll('.error-message').forEach((el) => {
        el.textContent = '';
        el.style.display = 'none';
    });
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    clearAllErrors();

    const validationResult = validateForm();

    if (!validationResult.isValid) {
        showNotification('Please fix the errors before submitting', 'error');
        return;
    }

    const formData = collectFormData();

    // YOUR AJAX SUBMISSION GOES HERE
    try {
        const response = await fetch('/meeting/create/', {
            method: 'POST',
            body: JSON.stringify(formData),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        if (!response.ok) {
            showNotification(
                'An error occurred whilst creating the meeting',
                'error',
            );
        }
        const data = await response.json();
        console.log(data);
        if (data.redirect) {
            window.location.href = data.redirect;
        }
        showNotification('Meeting was created', 'success');
    } catch (error) {
        console.log(error);
        showNotification(
            'An error occurred whilst creating the meeting',
            'error',
        );
    }
}

/**
 * Validate entire form
 */
function validateForm() {
    let isValid = true;
    const errors = [];

    // Validate title
    const title = document.getElementById('title');
    const titleError = validateTitle(title.value);
    if (titleError) {
        showErrorMessage(title, titleError);
        errors.push(titleError);
        isValid = false;
    }

    // Validate description
    const description = document.getElementById('description');
    const descError = validateDescription(description.value);
    if (descError) {
        showErrorMessage(description, descError);
        errors.push(descError);
        isValid = false;
    }

    // Validate duration
    const duration = document.getElementById('duration');
    const durationError = validateDuration(duration.value);
    if (durationError) {
        showErrorMessage(duration, durationError);
        errors.push(durationError);
        isValid = false;
    }

    // Validate questions
    const questions = document.querySelectorAll('.question-input');
    if (questions.length === 0) {
        showNotification('At least one question is required', 'error');
        errors.push('No questions');
        isValid = false;
    }

    questions.forEach((q) => {
        const error = validateQuestion(q.value);
        if (error) {
            showErrorMessage(q, error);
            errors.push(error);
            isValid = false;
        }
    });

    return { isValid, errors };
}

/**
 * Collect form data
 */
function collectFormData() {
    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();
    const duration = parseInt(document.getElementById('duration').value);
    const questions = Array.from(
        document.querySelectorAll('.question-input'),
    ).map((q) => q.value.trim());

    return { title, description, duration, questions };
}

/**
 * Show notification
 */
function showNotification(message, type = 'error') {
    const container = document.getElementById('notificationContainer');
    const notification = document.createElement('div');

    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span class="icon">${type === 'success' ? '✔' : '✖'}</span>
        <span>${message}</span>
    `;

    container.appendChild(notification);

    // Auto-dismiss
    setTimeout(() => {
        notification.classList.add('fadeOut');
        setTimeout(() => notification.remove(), 300);
    }, CONFIG.NOTIFICATION_DURATION);

    // Click to dismiss
    notification.addEventListener('click', () => {
        notification.classList.add('fadeOut');
        setTimeout(() => notification.remove(), 300);
    });
}

/**
 * Retrieves the CSRF Token embedded in the html file
 * @returns {*} Csrf Token String
 */
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
