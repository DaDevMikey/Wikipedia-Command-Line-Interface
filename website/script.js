document.addEventListener('DOMContentLoaded', () => {
  // Typing animation
  const commands = [
    'search Python programming',
    'view Python (programming language)',
    'images',
    'image 1',
    'links'
  ];
  
  let currentCommand = 0;
  let currentChar = 0;
  const typingElement = document.querySelector('.typing');
  
  function typeCommand() {
    if (currentChar < commands[currentCommand].length) {
      typingElement.textContent = commands[currentCommand].substring(0, currentChar + 1);
      currentChar++;
      setTimeout(typeCommand, 100);
    } else {
      setTimeout(() => {
        currentChar = 0;
        currentCommand = (currentCommand + 1) % commands.length;
        typingElement.textContent = '';
        typeCommand();
      }, 2000);
    }
  }
  
  typeCommand();

  // Smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });

  // Smooth entrance animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0) scale(1)';
      }
    });
  }, observerOptions);

  document.querySelectorAll('.floating-section, .feature-card').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px) scale(0.95)';
    element.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    observer.observe(element);
  });

  // Add ripple effect to buttons
  document.querySelectorAll('.download-button').forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      this.appendChild(ripple);
      
      const rect = button.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      ripple.addEventListener('animationend', () => {
        ripple.remove();
      });
    });
  });
});
