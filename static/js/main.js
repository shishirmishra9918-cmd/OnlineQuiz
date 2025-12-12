// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Add animations to elements with the fade-in class
    const fadeElements = document.querySelectorAll('.animate-fade-in');
    fadeElements.forEach((element, index) => {
        element.style.opacity = '0';
        setTimeout(() => {
            element.style.animation = 'fadeIn 0.5s ease forwards';
        }, index * 100);
    });
    
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                const bsAlert = new bootstrap.Alert(message);
                bsAlert.close();
            });
        }, 5000);
    }
    
    // Enhance quiz option selection UX
    const optionCards = document.querySelectorAll('.option-card');
    optionCards.forEach(card => {
        card.addEventListener('click', function() {
            // Find radio input within this option
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                
                // Remove active class from all options
                optionCards.forEach(c => c.classList.remove('active-option'));
                
                // Add active class to selected option
                this.classList.add('active-option');
            }
        });
    });
    
    // Quiz timer functionality (if present on page)
    const timerElement = document.getElementById('quiz-timer');
    if (timerElement) {
        let timeLeft = parseInt(timerElement.dataset.time || 300);
        
        const updateTimer = () => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            
            timerElement.innerHTML = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            
            if (timeLeft <= 30) {
                timerElement.classList.add('text-danger');
            }
            
            if (timeLeft <= 0) {
                // Auto-submit the form when time expires
                const quizForm = document.getElementById('questionForm');
                if (quizForm) {
                    quizForm.submit();
                }
                return;
            }
            
            timeLeft--;
            setTimeout(updateTimer, 1000);
        };
        
        updateTimer();
    }
    
    // Confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});