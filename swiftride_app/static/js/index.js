// navbar
// document.getElementById("userBtn").addEventListener("click", function(event) {
//   event.stopPropagation(); // Prevents closing immediately
//   const dropdown = document.querySelector(".user-dropdown");
//   dropdown.classList.toggle("open");
// });

// // Close dropdown when clicking outside
// window.addEventListener("click", function() {
//   const dropdown = document.querySelector(".user-dropdown");
//   dropdown.classList.remove("open");
// });
// navbar





//     function showPage(page) {
//     // hide all sections
//     document.querySelectorAll(".page-container").forEach(sec => {
//       sec.style.display = "none";
//     });

//     // show selected section
//     const section = document.getElementById(page + "-page");
//     if (section) section.style.display = "block";

//     // footer toggle
//     const footer = document.getElementById("main-footer");
//     if (page === "ride") {
//       footer.style.display = "none";   // hide footer on Ride page
//     } else {
//       footer.style.display = "block";  // show footer on other pages
//     }
//   }

//   // default page = home
//   showPage("home");
  
// // Password visibility toggle
//     function togglePassword(inputId, toggleIcon) {
//   const input = document.getElementById(inputId);
//   if (input.type === "password") {
//     input.type = "text";
//     toggleIcon.textContent = "🙈"; // password visible
//   } else {
//     input.type = "password";
//     toggleIcon.textContent = "👁️"; // password hidden
//   }
// }

//     window.addEventListener("scroll", function () {
//       const navbar = document.querySelector(".navbar");
//       if (window.scrollY > 50) { // 50px down from top
//         navbar.classList.add("scrolled");
//       } else {
//         navbar.classList.remove("scrolled");
//       }
//     });
//     function toggleTheme() {
//       document.body.classList.toggle("dark-mode");
//       const btn = document.querySelector(".theme-toggle");

//       if (document.body.classList.contains("dark-mode")) {
//         btn.textContent = "💡"; // glowing bulb in dark mode
//       } else {
//         btn.textContent = "🔆"; // sun/light symbol in light mode
//       }
//     }
//     // Page navigation
//     function showPage(pageId) {
//       // Hide all pages
//       document.querySelectorAll('.page-container').forEach(page => {
//         page.classList.remove('active');
//       });

//       // Show the selected page
//       document.getElementById(pageId + '-page').classList.add('active');

//       // Update navigation
//       document.querySelectorAll('.nav-link').forEach(link => {
//         link.classList.remove('active');
//       });

//       // Find and activate the current nav link
//       const activeLink = Array.from(document.querySelectorAll('.nav-link')).find(link => {
//         return link.textContent.toLowerCase().includes(pageId);
//       });

//       if (activeLink) {
//         activeLink.classList.add('active');
//       }
//     }

//     // Form step navigation
//     function showStep(stepNumber) {
//       // Hide all steps
//       document.querySelectorAll('.form-step').forEach(step => {
//         step.classList.remove('active');
//       });

//       // Show the selected step
//       document.getElementById('step' + stepNumber).classList.add('active');

//       // Update progress steps
//       document.querySelectorAll('.progress-step').forEach((step, index) => {
//         if (index + 1 < stepNumber) {
//           step.classList.add('completed');
//           step.classList.remove('active');
//         } else if (index + 1 === stepNumber) {
//           step.classList.add('active');
//           step.classList.remove('completed');
//         } else {
//           step.classList.remove('active', 'completed');
//         }
//       });
//     }
//   function nextStep(currentStep) {
//   let valid = true;

//   // Step 1: Personal Info
//   if (currentStep === 1) {
//     const firstName = document.getElementById('firstName').value.trim();
//     const lastName = document.getElementById('lastName').value.trim();
//     const email = document.getElementById('email').value.trim();
//     const phone = document.getElementById('phone').value.trim();

//     if (!firstName || !lastName || !email || !phone) {
//       alert('Please fill all required fields in Step 1');
//       valid = false;
//     } else if (!/^\d{10}$/.test(phone)) {
//       document.getElementById('phoneError').style.display = 'block';
//       valid = false;
//     } else {
//       document.getElementById('phoneError').style.display = 'none';
//     }
//   }

//   // Step 2: Password Info
//   if (currentStep === 2) {
//     const password = document.getElementById('password').value;
//     const confirmPassword = document.getElementById('confirmPassword').value;

//     if (!password || !confirmPassword) {
//       alert('Please fill all required fields in Step 2');
//       valid = false;
//     } else if (password !== confirmPassword) {
//       alert('Passwords do not match');
//       valid = false;
//     }
//   }

//   // Step 3: Additional Info
//   if (currentStep === 3) {
//     const address = document.getElementById('address').value.trim();
//     const state = document.getElementById('state').value.trim();
//     const city = document.getElementById('city').value.trim();
//     const zipCode = document.getElementById('zipCode').value.trim();
//     const terms = document.getElementById('terms').checked;

//     if (!address || !state || !city || !zipCode) {
//       alert('Please fill all required fields in Step 3');
//       valid = false;
//     } else if (!terms) {
//       alert('You must accept Terms of Service to continue');
//       valid = false;
//     }
//   }

//   if (valid) {
//     showStep(currentStep + 1);
//   }
// }


// // Similarly, your Back button can just call showStep(currentStep - 1)


//     // Password strength indicator
//     function checkPasswordStrength() {
//       const password = document.getElementById('password').value;
//       const strengthBar = document.getElementById('passwordStrength');
//       const helpText = document.getElementById('passwordHelp');

//       // Reset
//       strengthBar.style.width = '0';
//       strengthBar.style.background = '#ddd';

//       if (password.length === 0) {
//         helpText.textContent = 'Use at least 8 characters with a mix of letters, numbers & symbols';
//         helpText.style.color = 'var(--gray)';
//         return;
//       }

//       // Check password strength
//       let strength = 0;

//       // Length check
//       if (password.length >= 8) strength += 20;

//       // Contains both lower and uppercase characters
//       if (password.match(/([a-z].[A-Z])|([A-Z].[a-z])/)) strength += 20;

//       // Contains numbers
//       if (password.match(/([0-9])/)) strength += 20;

//       // Contains special characters
//       if (password.match(/([!,@,#,$,%,^,&,*,?,_,~])/)) strength += 20;

//       // Contains both letters and numbers
//       if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 20;

//       // Update UI
//       strengthBar.style.width = strength + '%';

//       if (strength < 40) {
//         strengthBar.style.background = '#dc3545';
//         helpText.textContent = 'Weak password';
//         helpText.style.color = '#dc3545';
//       } else if (strength < 80) {
//         strengthBar.style.background = '#ffc107';
//         helpText.textContent = 'Medium strength password';
//         helpText.style.color = '#ffc107';
//       } else {
//         strengthBar.style.background = '#28a745';
//         helpText.textContent = 'Strong password!';
//         helpText.style.color = '#28a745';
//       }
//     }

//     // Password confirmation validation
//     function validatePassword() {
//       const password = document.getElementById('password').value;
//       const confirmPassword = document.getElementById('confirmPassword').value;
//       const matchText = document.getElementById('passwordMatch');

//       if (confirmPassword.length > 0 && password !== confirmPassword) {
//         matchText.style.display = 'block';
//       } else {
//         matchText.style.display = 'none';
//       }
//     }

//     // Form validation and submission
//     document.addEventListener('DOMContentLoaded', function () {
//       const forms = document.querySelectorAll('form');

//       forms.forEach(form => {
//         form.addEventListener('submit', function (e) {
//           e.preventDefault();

//           if (form.id === 'login-form') {
//             // Login form submission
//             alert('Login successful! In a real application, this would authenticate your credentials.');
//             showPage('home');
//           } else {
//             // Signup form submission
//             alert('Account created successfully! In a real application, this would submit your data.');
//             showPage('home');
//           }
//         });
//       });
      
   


//       // Add animation to the form elements
//       const inputs = document.querySelectorAll('input');
//       inputs.forEach(input => {
//         input.addEventListener('focus', function () {
//           this.parentElement.style.transform = 'scale(1.02)';
//           this.parentElement.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
//         });

//         input.addEventListener('blur', function () {
//           this.parentElement.style.transform = 'scale(1)';
//           this.parentElement.style.boxShadow = 'none';
//         });
//       });

//       // Add floating animation to the main container
//       const mainContainers = document.querySelectorAll('.main-container');
//       mainContainers.forEach(container => {
//         container.style.opacity = '0';
//         container.style.transform = 'translateY(20px)';

//         setTimeout(() => {
//           container.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
//           container.style.opacity = '1';
//           container.style.transform = 'translateY(0)';
//         }, 100);
//       });
//     });
//     document.addEventListener('DOMContentLoaded', function () {
//       // --- Input animations ---
//       const inputs = document.querySelectorAll('input');
//       inputs.forEach(input => {
//         input.addEventListener('focus', function () {
//           this.parentElement.style.transform = 'scale(1.02)';
//           this.parentElement.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
//         });
//         input.addEventListener('blur', function () {
//           this.parentElement.style.transform = 'scale(1)';
//           this.parentElement.style.boxShadow = 'none';
//         });
//       });

//       // --- Floating animation for main containers ---
//       const mainContainers = document.querySelectorAll('.main-container');
//       mainContainers.forEach(container => {
//         container.style.opacity = '0';
//         container.style.transform = 'translateY(20px)';
//         setTimeout(() => {
//           container.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
//           container.style.opacity = '1';
//           container.style.transform = 'translateY(0)';
//         }, 100);
//       });
//     });

    

// const loginForm = document.getElementById('login-form');
// if (loginForm) {
//   loginForm.addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const email = document.getElementById('login-email').value.trim();
//     const password = document.getElementById('login-password').value;

//     try {
//       const res = await fetch('/login', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         credentials: 'include', // include cookies for session
//         body: JSON.stringify({ email, password })
//       });

//       const json = await res.json().catch(() => ({}));

//       // handle common errors
//       if (res.status === 404) {
//         alert(json.error || 'This email is not registered. Please sign up.');
//         return;
//       }
//       if (res.status === 401) {
//         alert(json.error || 'Incorrect password. Try again.');
//         return;
//       }
//       if (!res.ok) {
//         alert(json.error || 'Server error. Try again later.');
//         return;
//       }

//       // Login succeeded on backend; fetch current user data from /me
//       try {
//         const meRes = await fetch('/me', { credentials: 'include' });
//         if (meRes.ok) {
//           const meJson = await meRes.json();
//           // backend returns { user: {...} } — support both shapes
//           const userObj = meJson.user ? meJson.user : meJson;
//           // store in sessionStorage for dashboard to read (optional)
//           sessionStorage.setItem('sr_user', JSON.stringify(userObj));
//         } else {
//           // if /me failed, still proceed to dashboard (server session exists)
//           console.warn('/me fetch failed after login, status:', meRes.status);
//         }
//       } catch (errMe) {
//         console.warn('Failed to fetch /me after login:', errMe);
//       }

//       // Optional: short success message then redirect
//       // alert(json.message || 'Login successful!');
//       window.location.href = '/dashboard'; // go to the separate dashboard page

//     } catch (err) {
//       console.error(err);
//       alert('Network error. Is the backend running?');
//     }
//   });
// }

//     // SIGNUP handler (final step form id="step3")
//     const signupFinal = document.getElementById('step3');
//     if (signupFinal) {
//       signupFinal.addEventListener('submit', async (e) => {
//         e.preventDefault();
//         const userData = {
//           firstName: document.getElementById('firstName').value.trim(),
//           lastName: document.getElementById('lastName').value.trim(),
//           email: document.getElementById('email').value.trim(),
//           phone: document.getElementById('phone').value.trim(),
//           password: document.getElementById('password').value,
//           address: document.getElementById('address').value.trim(),
//           state: document.getElementById('state').value.trim(),
//           city: document.getElementById('city').value.trim(),
//           zipCode: document.getElementById('zipCode').value.trim(),
//           preferredPayment: document.getElementById('preferredPayment').value
//         };
//         // --- PHONE VALIDATION ---
//     if (!/^[0-9]{10}$/.test(userData.phone)) {
//       alert("Please enter a valid 10-digit phone number");
//       document.getElementById('phone').style.borderColor = 'red';
//       return; // stop submission if invalid
//     } else {
//       document.getElementById('phone').style.borderColor = 'green';
//     }

//         try {
//           const res = await fetch('/signup', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify(userData)
//           });
//           const json = await res.json();

//           if (res.status === 409) {
//             alert(json.error || 'Email already registered. Please login.');
//             return;
//           }
//           if (!res.ok) {
//             alert(json.error || 'Server error. Try again later.');
//             return;
//           }

//           alert(json.message || 'Account created!');
//           showPage('login');
//         } catch (err) {
//           console.error(err);
//           alert('Network error. Is the backend running?');
//         }
//       });
//     }
//     // --- Phone validation ---
// const phoneInput = document.getElementById("phone");
// const phoneError = document.getElementById("phoneError");

// if (phoneInput) {
//   phoneInput.addEventListener("input", function () {
//     // Only keep digits
//     phoneInput.value = phoneInput.value.replace(/\D/g, "");

//     const value = phoneInput.value;
//     const isValid = /^[0-9]{10}$/.test(value);

//     if (!isValid) {
//       phoneInput.style.borderColor = "red";
//       phoneError.style.display = "block";
//     } else {
//       phoneInput.style.borderColor = "green";
//       phoneError.style.display = "none";
//     }
//   });
// }

//     const stateCityMap = {
//       "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
//       "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
//       "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi"],
//       "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket", "Karol Bagh"]
//       // you can keep adding more states & cities here
//     };

//     document.getElementById("state").addEventListener("change", function () {
//       const state = this.value;
//       const citySelect = document.getElementById("city");

//       // clear old options
//       citySelect.innerHTML = '<option value="">Select your city</option>';

//       if (state && stateCityMap[state]) {
//         stateCityMap[state].forEach(city => {
//           const opt = document.createElement("option");
//           opt.value = city;
//           opt.textContent = city;
//           citySelect.appendChild(opt);
//         });
//       }
//     });



/* ---------- Unified app script for SwiftRide (replace your existing JS) ---------- */

(function () {
  'use strict';

  /* ---------- Page navigation & footer ---------- */
  function showPage(pageId) {
    // hide all pages (use display:block/none for robustness)
    document.querySelectorAll('.page-container').forEach(p => {
      p.style.display = 'none';
      p.classList.remove('active');
    });

    const target = document.getElementById(pageId + '-page');
    if (target) {
      target.style.display = 'block';
      target.classList.add('active');
    }

    // footer toggle
    const footer = document.getElementById('main-footer');
    if (footer) footer.style.display = (pageId === 'ride') ? 'none' : 'block';

    // update nav-link active class (if nav links exist)
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    const navLinks = Array.from(document.querySelectorAll('.nav-link'));
    const found = navLinks.find(link => link.getAttribute('onclick')?.includes(pageId) ||
      (link.textContent && link.textContent.trim().toLowerCase().includes(pageId)));
    if (found) found.classList.add('active');
  }

  // default page: home
  if (!document.querySelector('.page-container.active')) showPage('home');

  /* ---------- Password toggle & strength ---------- */
  window.togglePassword = function (inputId, toggleIconElem) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === 'password') {
      input.type = 'text';
      if (toggleIconElem) toggleIconElem.textContent = '🙈';
    } else {
      input.type = 'password';
      if (toggleIconElem) toggleIconElem.textContent = '👁️';
    }
  };

  function checkPasswordStrength() {
    const pw = document.getElementById('password');
    const strengthBar = document.getElementById('passwordStrength');
    const helpText = document.getElementById('passwordHelp');
    if (!pw || !strengthBar || !helpText) return;

    const password = pw.value || '';
    let strength = 0;

    if (password.length >= 8) strength += 20;
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 20;
    if (password.match(/[0-9]/)) strength += 20;
    if (password.match(/[!@#$%^&*?_~\-,.]/)) strength += 20;
    if (password.match(/[a-zA-Z]/) && password.match(/[0-9]/)) strength += 20;

    strengthBar.style.width = strength + '%';
    if (strength < 40) {
      strengthBar.style.background = '#dc3545';
      helpText.textContent = 'Weak password';
      helpText.style.color = '#dc3545';
    } else if (strength < 80) {
      strengthBar.style.background = '#ffc107';
      helpText.textContent = 'Medium strength password';
      helpText.style.color = '#ffc107';
    } else {
      strengthBar.style.background = '#28a745';
      helpText.textContent = 'Strong password!';
      helpText.style.color = '#28a745';
    }
  }

  window.checkPasswordStrength = checkPasswordStrength;

  function validatePasswordMatch() {
    const pw = document.getElementById('password');
    const cpw = document.getElementById('confirmPassword');
    const matchText = document.getElementById('passwordMatch');
    if (!pw || !cpw || !matchText) return;
    matchText.style.display = (cpw.value && pw.value !== cpw.value) ? 'block' : 'none';
  }
  window.validatePassword = validatePasswordMatch;

  /* ---------- Scroll nav class ---------- */
  window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    if (window.scrollY > 50) navbar.classList.add('scrolled'); else navbar.classList.remove('scrolled');
  });

  /* ---------- Theme toggle ---------- */
  window.toggleTheme = function () {
    document.body.classList.toggle('dark-mode');
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    btn.textContent = document.body.classList.contains('dark-mode') ? '💡' : '🔆';
  };

  /* ---------- Form step controls ---------- */
  function showStep(stepNumber) {
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
    const el = document.getElementById('step' + stepNumber);
    if (el) el.classList.add('active');

    document.querySelectorAll('.progress-step').forEach((step, idx) => {
      step.classList.remove('active', 'completed');
      if (idx + 1 < stepNumber) step.classList.add('completed');
      else if (idx + 1 === stepNumber) step.classList.add('active');
    });
  }
  window.showStep = showStep;

  function nextStep(currentStep) {
    let valid = true;
    // Step 1
    if (currentStep === 1) {
      const firstName = (document.getElementById('firstName') || {}).value?.trim();
      const lastName = (document.getElementById('lastName') || {}).value?.trim();
      const email = (document.getElementById('email') || {}).value?.trim();
      const phone = (document.getElementById('phone') || {}).value?.trim();
      const phoneError = document.getElementById('phoneError');
      if (!firstName || !lastName || !email || !phone) {
        alert('Please fill all required fields in Step 1');
        valid = false;
      } else if (!/^\d{10}$/.test(phone)) {
        if (phoneError) phoneError.style.display = 'block';
        valid = false;
      } else if (phoneError) phoneError.style.display = 'none';
    }
    // Step 2
    if (currentStep === 2) {
      const password = (document.getElementById('password') || {}).value;
      const confirmPassword = (document.getElementById('confirmPassword') || {}).value;
      if (!password || !confirmPassword) {
        alert('Please fill all required fields in Step 2');
        valid = false;
      } else if (password !== confirmPassword) {
        alert('Passwords do not match');
        valid = false;
      }
    }
    // Step 3 - we typically submit here so validation optional
    if (valid) showStep(currentStep + 1);
  }
  window.nextStep = nextStep;

  /* ---------- Animations for inputs / containers (safe) ---------- */
  function initAnimations() {
    document.querySelectorAll('input').forEach(input => {
      input.addEventListener('focus', function () {
        if (this.parentElement) {
          this.parentElement.style.transform = 'scale(1.02)';
          this.parentElement.style.boxShadow = '0 5px 15px rgba(0,0,0,0.08)';
        }
      });
      input.addEventListener('blur', function () {
        if (this.parentElement) {
          this.parentElement.style.transform = 'scale(1)';
          this.parentElement.style.boxShadow = 'none';
        }
      });
    });

    document.querySelectorAll('.main-container').forEach(container => {
      container.style.opacity = '0';
      container.style.transform = 'translateY(20px)';
      setTimeout(() => {
        container.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
      }, 100);
    });
  }

  /* ---------- Login handler (calls /login and includes cookies) ---------- */
  function initAuthHandlers() {
    // const loginForm = document.getElementById('login-form');
    // if (loginForm) {
    //   loginForm.addEventListener('submit', async (e) => {
    //     e.preventDefault();
    //     const email = (document.getElementById('login-email') || {}).value?.trim();
    //     const password = (document.getElementById('login-password') || {}).value || '';
    //     if (!email || !password) { alert('Enter email and password'); return; }

    //     try {
    //       const res = await fetch('/login', {
    //         method: 'POST',
    //         headers: { 'Content-Type': 'application/json' },
    //         credentials: 'include', // important: include cookies
    //         body: JSON.stringify({ email, password })
    //       });

    //       const json = await res.json().catch(() => ({}));
    //       if (res.status === 401 || res.status === 404) {
    //         alert(json.error || 'Login failed');
    //         return;
    //       }
    //       if (!res.ok) {
    //         alert(json.error || 'Server error. Try again later.');
    //         return;
    //       }

    //       // On success: redirect to dashboard (you have /dashboard route)
    //       window.location.href = '/dashboard';
    //     } catch (err) {
    //       console.error('Login error', err);
    //       alert('Network error. Is the backend running?');
    //     }
    //   });
    // }
    // login handler (ensure credentials: 'include')
const loginForm = document.getElementById('login-form');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    const res = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',   // IMPORTANT: include cookies so Flask session is set
      body: JSON.stringify({ email, password })
    });

    if (res.ok) {
      // simplest: reload homepage so Jinja shows authenticated navbar
      window.location.href = '/';   // or window.location.reload();
      // or redirect to /dashboard: window.location.href = '/dashboard';
    } else {
      const json = await res.json().catch(()=>({}));
      alert(json.error || 'Login failed');
    }
  });
}


    // Signup: final step form (#step3 is a form) -> POST to /signup
    const signupForm = document.getElementById('step3');
    if (signupForm) {
      signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userData = {
          firstName: (document.getElementById('firstName') || {}).value?.trim(),
          lastName: (document.getElementById('lastName') || {}).value?.trim(),
          email: (document.getElementById('email') || {}).value?.trim(),
          phone: (document.getElementById('phone') || {}).value?.trim(),
          password: (document.getElementById('password') || {}).value || '',
          address: (document.getElementById('address') || {}).value?.trim() || '',
          state: (document.getElementById('state') || {}).value?.trim() || '',
          city: (document.getElementById('city') || {}).value?.trim() || '',
          zipCode: (document.getElementById('zipCode') || {}).value?.trim() || '',
          preferredPayment: (document.getElementById('preferredPayment') || {}).value || ''
        };

        if (!/^\d{10}$/.test(userData.phone)) { alert('Please enter valid 10-digit phone'); return; }

        try {
          const res = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(userData)
          });
          const json = await res.json().catch(() => ({}));
          if (res.status === 409) { alert(json.error || 'Email exists. Please login.'); return; }
          if (!res.ok) { alert(json.error || 'Signup failed'); return; }

          alert(json.message || 'Account created!');
          showPage('login');
        } catch (err) {
          console.error('Signup error', err);
          alert('Network error. Is the backend running?');
        }
      });
    }

    // Logout button (if present, id="logout-btn")
    // const logoutBtn = document.getElementById('logout-btn');
    // if (logoutBtn) {
    //   logoutBtn.addEventListener('click', async (e) => {
    //     e.preventDefault();
    //     try {
    //       const res = await fetch('/logout', { method: 'POST', credentials: 'include' });
    //       if (res.ok) window.location.href = '/';
    //     } catch (err) { console.error('Logout failed', err); }
    //   });
    // }
      const userBtn = document.getElementById("userBtn");
  const dropdown = document.querySelector(".user-dropdown");

  if (userBtn) {
    userBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      dropdown.classList.toggle("open");
    });
  }

  // Close dropdown when clicking outside
  window.addEventListener("click", () => {
    dropdown?.classList.remove("open");
  });

  // Logout handler
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        const res = await fetch('/logout', {
          method: 'POST',
          credentials: 'include'
        });
        if (res.ok) {
          window.location.href = '/'; // redirect to home page after logout
        } else {
          console.error('Logout failed');
        }
      } catch (err) {
        console.error('Logout failed', err);
      }
    });
  }

  }


  

  /* ---------- Phone input live validation ---------- */
  function initPhoneValidation() {
    const phoneInput = document.getElementById('phone');
    const phoneError = document.getElementById('phoneError');
    if (!phoneInput) return;
    phoneInput.addEventListener('input', () => {
      phoneInput.value = phoneInput.value.replace(/\D/g, '');
      const valid = /^\d{10}$/.test(phoneInput.value);
      phoneInput.style.borderColor = valid ? 'green' : 'red';
      if (phoneError) phoneError.style.display = valid ? 'none' : 'block';
    });
  }

  /* ---------- State -> City mapping ---------- */
  function initStateCity() {
    const stateCityMap = {
      "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
      "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
      "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi"],
      "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket", "Karol Bagh"]
    };
    const stateSel = document.getElementById('state');
    const citySel = document.getElementById('city');
    if (!stateSel || !citySel) return;
    stateSel.addEventListener('change', function () {
      citySel.innerHTML = '<option value="">Select your city</option>';
      const arr = stateCityMap[this.value];
      if (Array.isArray(arr)) {
        arr.forEach(c => {
          const opt = document.createElement('option'); opt.value = c; opt.textContent = c; citySel.appendChild(opt);
        });
      }
    });
  }

  /* ---------- Init on DOM ready ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    initAnimations();
    initAuthHandlers();
    initPhoneValidation();
    initStateCity();

    // hook password strength & confirm listeners (if inputs exist)
    const pw = document.getElementById('password');
    if (pw) pw.addEventListener('input', checkPasswordStrength);
    const cpw = document.getElementById('confirmPassword');
    if (cpw) cpw.addEventListener('input', validatePasswordMatch);
  });

})();





















    // Initialize the map
    // function initMap() {
    //   // Pune coordinates
    //   const pune = { lat: 18.5204, lng: 73.8567 };

    //   // Create map centered at Pune
    //   const map = new google.maps.Map(document.getElementById("map"), {
    //     zoom: 12,
    //     center: pune,
    //   });

    //   // Add marker for Pune
    //   new google.maps.Marker({
    //     position: pune,
    //     map: map,
    //     title: "Pune City",
    //   });
    // }


// 
// --- JAVASCRIPT FIX: Update your existing initMappls function ---

function initMappls() { // We keep the name initMappls to avoid changing showPage()
    if (rideMap) return;

    const mapContainer = document.getElementById("map-container");
    if (!mapContainer) return;

    // Pune Coordinates [Latitude, Longitude]
    const puneCoords = [18.5204, 73.8567]; 
    
    try {
        // 1. Create the map instance (Leaflet uses L.map)
        rideMap = L.map("map-container").setView(puneCoords, 12); 
        
        // 2. Add OpenStreetMap Tiles as the base layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors' // Attribution is mandatory for OSM
        }).addTo(rideMap);

        // 3. Add an initial marker for context
        L.marker(puneCoords).addTo(rideMap)
            .bindPopup("Pune City Center").openPopup();

        // 4. CRITICAL FIX: Tell the map to recalculate size (from previous fix)
        // Note: Leaflet stores the map instance as L.map(id), not rideMap.invalidateSize()
        setTimeout(function() {
            if (rideMap) {
                rideMap.invalidateSize();
            }
        }, 100);

        console.log("Leaflet/OSM Map Initialized successfully.");
        
    } catch (e) {
        console.error("Error initializing Leaflet Map:", e);
    }
}
// --------------------------------------------------------------------------
// --- Updated showPage function ---
function showPage(page) {
    // 1. Hide all sections
    document.querySelectorAll(".page-container").forEach(sec => {
        sec.style.display = "none";
        sec.classList.remove("active"); // Remove active class first
    });

    // 2. Show selected section
    const section = document.getElementById(page + "-page");
    if (section) {
        section.style.display = "flex"; // Changed from 'block' to 'flex' to maintain center
        section.classList.add("active");
    }

    // 3. Footer toggle (already in your code)
    const footer = document.getElementById("main-footer");
    if (page === "ride") {
        footer.style.display = "none"; 
        // CRUCIAL: Initialize map when ride page is displayed
        // initMappls(); 
         setTimeout(initMappls, 50);
    } else {
        footer.style.display = "block";
    }
    
    // 4. Update nav links (already in your code)
    // ... (rest of your existing showPage and nav link update logic)
}

// Make sure to call showPage("home") or showPage("ride") initially
// showPage("home");
// // --- SESSION CHECK ---
// async function checkSession() {
//   try {
//     const res = await fetch("/me");
//     if (res.ok) {
//       const data = await res.json();
//       const user = data.user;
//       showLoggedIn(user.firstName);
//     } else {
//       showLoggedOut();
//     }
//   } catch (err) {
//     console.error("Session check failed", err);
//     showLoggedOut();
//   }
// }

// // --- LOGOUT ---
// async function logout() {
//   await fetch("/logout", { method: "POST" });
//   showLoggedOut();
//   showPage("home");
// }

// // --- UI Updates ---
// function showLoggedIn(username) {
//   document.getElementById("welcome-message").style.display = "block";
//   document.getElementById("user-name").textContent = username;

//   document.getElementById("nav-links").innerHTML = `
//     <a class="nav-link" href="#" onclick="showPage('home')">Home</a>
//     <a class="nav-link" href="#" onclick="showPage('ride')">Ride</a>
//     <a class="nav-link" href="#" onclick="showPage('profile')">Profile</a>
//     <a class="nav-link" href="#" onclick="logout()">Logout</a>
//     <button class="theme-toggle" onclick="toggleTheme()">💡</button>
//   `;
// }

// function showLoggedOut() {
//   document.getElementById("welcome-message").style.display = "none";

//   document.getElementById("nav-links").innerHTML = `
//     <a class="nav-link" href="#" onclick="showPage('home')">Home</a>
//     <a class="nav-link" href="#" onclick="showPage('ride')">Ride</a>
//     <a class="nav-link" href="#" onclick="showPage('login')">Login</a>
//     <a class="nav-link" href="#" onclick="showPage('signup')">Sign Up</a>
//     <button class="theme-toggle" onclick="toggleTheme()">💡</button>
//   `;
// }

// // Run session check once DOM is ready
// document.addEventListener("DOMContentLoaded", checkSession);




    // new page
   //  ride polling 
//    async function showPrice() {
//   const data = {
//     D_AC: parseFloat(document.getElementById("d_ac").value),
//     D_Shared: parseFloat(document.getElementById("d_shared").value),
//     D_P_Exclusive: parseFloat(document.getElementById("d_exclusive").value),
//     P_Exclusive_Owner: document.getElementById("owner").value
//   };

//   try {
//     const res = await fetch("http://localhost:5000/calculate_fare", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(data)
//     });

//     const result = await res.json();

//     if (res.ok) {
//       document.getElementById("price-output").innerHTML = `
//         <strong>P1 Fare:</strong> ₹${result.fare_pooled.P1_Requester}<br>
//         <strong>P2 Fare:</strong> ₹${result.fare_pooled.P2_Sharer}<br>
//         <strong>Total Paid:</strong> ₹${result.fare_pooled.total_paid}<br>
//         <strong>Solo Fare (P1):</strong> ₹${result.fare_solo_p1}<br>
//         <strong>Savings (P1):</strong> ₹${result.savings_p1}
//       `;
//     } else {
//       document.getElementById("price-output").innerText = result.error || "Something went wrong!";
//     }
//   } catch (err) {
//     document.getElementById("price-output").innerText = "Server error: " + err.message;
//   }
// }











// Handle login form
// Handle login form submission
// document.getElementById("login-form").addEventListener("submit", function (e) {
//   e.preventDefault();

//   const email = document.getElementById("login-email").value;
//   const password = document.getElementById("login-password").value;

//   if (email && password) {
//     const userData = { email: email, name: email.split("@")[0] };
//     localStorage.setItem("swift_user", JSON.stringify(userData));

//     // Update navbar and show Ride page
//     updateNavbarForLogin();
//     showPage("ride");

//     alert("Welcome back, " + userData.name + " 👋");
//   } else {
//     alert("Please enter valid credentials.");
//   }
// });

// // Update navbar for logged-in user
// function updateNavbarForLogin() {
//   const user = JSON.parse(localStorage.getItem("swift_user"));
//   if (!user) return;

//   const navLinks = document.getElementById("nav-links");
//   navLinks.innerHTML = `
//     <a href="#" class="nav-link" onclick="showPage('ride')">Ride</a>
//     <span class="nav-welcome">Welcome, ${user.name} 👋</span>
//     <button class="logout-btn" onclick="logoutUser()">Logout</button>
//     <button class="theme-toggle" onclick="toggleTheme()">💡</button>
//   `;
// }

// // Logout function
// function logoutUser() {
//   localStorage.removeItem("swift_user");
//   location.reload(); // refresh page to reset to login
// }

// // Auto-detect login state on page load
// window.addEventListener("load", () => {
//   const user = JSON.parse(localStorage.getItem("swift_user"));
//   if (user) {
//     updateNavbarForLogin();
//     showPage("ride"); // directly show Ride page after login
//   } else {
//     showPage("login");
//   }
// });






// let rideMap, pickupMarker, dropMarker, routeLine;

// // Initialize map when ride page loads
// function initRideMap() {
//   if (!rideMap) {
//     rideMap = L.map("map-container").setView([18.5204, 73.8567], 12);

//     L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//       maxZoom: 19,
//       attribution: "&copy; OpenStreetMap contributors",
//     }).addTo(rideMap);
//   }
// }

// // Function to show price & route
// async function showPrice() {
//   const pickup = document.getElementById("pickup").value.trim();
//   const drop = document.getElementById("dropoff").value.trim();
//   const priceOutput = document.getElementById("price-output");

//   if (!pickup || !drop) {
//     alert("Please enter both pickup and dropoff locations.");
//     return;
//   }

//   initRideMap();

//   // Get coordinates using Nominatim API
//   const pickupCoords = await getCoordinates(pickup);
//   const dropCoords = await getCoordinates(drop);

//   if (!pickupCoords || !dropCoords) {
//     alert("Unable to locate one or both locations.");
//     return;
//   }

//   // Clear existing markers/route
//   if (pickupMarker) rideMap.removeLayer(pickupMarker);
//   if (dropMarker) rideMap.removeLayer(dropMarker);
//   if (routeLine) rideMap.removeLayer(routeLine);

//   // Add new markers
//   pickupMarker = L.marker(pickupCoords).addTo(rideMap).bindPopup("Pickup: " + pickup);
//   dropMarker = L.marker(dropCoords).addTo(rideMap).bindPopup("Drop: " + drop);

//   // Draw a straight line route
//   routeLine = L.polyline([pickupCoords, dropCoords], { color: "blue", weight: 4 }).addTo(rideMap);

//   // Zoom to fit both points
//   rideMap.fitBounds(L.latLngBounds([pickupCoords, dropCoords]), { padding: [50, 50] });

//   // Calculate distance (in km)
//   const distance = getDistance(pickupCoords, dropCoords);
//   const price = (distance * 15).toFixed(2); // ₹15 per km example

//   priceOutput.textContent = `Estimated Distance: ${distance.toFixed(2)} km | Price: ₹${price}`;
// }

// // Convert place name → coordinates using OpenStreetMap
// async function getCoordinates(location) {
//   try {
//     const response = await fetch(
//       `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`
//     );
//     const data = await response.json();
//     if (data.length > 0) {
//       return [parseFloat(data[0].lat), parseFloat(data[0].lon)];
//     }
//     return null;
//   } catch (err) {
//     console.error("Error fetching coordinates:", err);
//     return null;
//   }
// }

// // Haversine formula to calculate distance between two coordinates
// function getDistance(coord1, coord2) {
//   const R = 6371; // km
//   const dLat = (coord2[0] - coord1[0]) * Math.PI / 180;
//   const dLon = (coord2[1] - coord1[1]) * Math.PI / 180;
//   const a =
//     Math.sin(dLat / 2) ** 2 +
//     Math.cos(coord1[0] * Math.PI / 180) *
//       Math.cos(coord2[0] * Math.PI / 180) *
//       Math.sin(dLon / 2) ** 2;
//   const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//   return R * c;
// }

// 22-10-25***********
// let rideMap, pickupMarker, dropMarker, routeLine;
// let pickupTimeout = null;
// let dropoffTimeout = null;

// // Initialize map when ride page loads
// function initRideMap() {
//   if (!rideMap) {
//     rideMap = L.map("map-container").setView([18.5204, 73.8567], 12);

//     L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//       maxZoom: 19,
//       attribution: "&copy; OpenStreetMap contributors",
//     }).addTo(rideMap);
//   }
// }

// // Convert place name → coordinates using OpenStreetMap Nominatim
// async function getCoordinates(location) {
//   try {
//     const response = await fetch(
//       `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
//         location
//       )}&limit=1`,
//       {
//         headers: {
//           "User-Agent": "RideShareApp/1.0", // Nominatim requires user agent
//         },
//       }
//     );
//     const data = await response.json();
//     if (data.length > 0) {
//       return [parseFloat(data[0].lat), parseFloat(data[0].lon)];
//     }
//     return null;
//   } catch (err) {
//     console.error("Error fetching coordinates:", err);
//     return null;
//   }
// }

// // Haversine formula to calculate distance between two coordinates
// function getDistance(coord1, coord2) {
//   const R = 6371; // Earth radius in km
//   const dLat = ((coord2[0] - coord1[0]) * Math.PI) / 180;
//   const dLon = ((coord2[1] - coord1[1]) * Math.PI) / 180;
//   const a =
//     Math.sin(dLat / 2) ** 2 +
//     Math.cos((coord1[0] * Math.PI) / 180) *
//       Math.cos((coord2[0] * Math.PI) / 180) *
//       Math.sin(dLon / 2) ** 2;
//   const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//   return R * c;
// }

// // 🧠 Live pickup marker update
// async function updatePickupLocation(query) {
//   if (!query || query.trim() === "") {
//     // Remove marker if input is empty
//     if (pickupMarker) {
//       rideMap.removeLayer(pickupMarker);
//       pickupMarker = null;
//       if (routeLine) {
//         rideMap.removeLayer(routeLine);
//         routeLine = null;
//       }
//     }
//     return;
//   }

//   const coords = await getCoordinates(query);
//   if (!coords) {
//     console.log("Could not find location for:", query);
//     return;
//   }

//   // Initialize map if not yet created
//   initRideMap();

//   // Remove old pickup marker
//   if (pickupMarker) rideMap.removeLayer(pickupMarker);

//   // Create custom green marker for pickup
//   const pickupIcon = L.divIcon({
//     className: "custom-marker",
//     html: '<div style="background: #10b981; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
//     iconSize: [30, 30],
//     iconAnchor: [15, 15],
//   });

//   // Add new pickup marker
//   pickupMarker = L.marker(coords, { icon: pickupIcon })
//     .addTo(rideMap)
//     .bindPopup(`<b>📍 Pickup</b><br>${query}`)
//     .openPopup();

//   // Center map smoothly
//   rideMap.setView(coords, 14);

//   // If drop marker exists, draw route
//   updateRoute();
// }

// // 🧠 Live dropoff marker update
// async function updateDropoffLocation(query) {
//   if (!query || query.trim() === "") {
//     if (dropMarker) {
//       rideMap.removeLayer(dropMarker);
//       dropMarker = null;
//     }
//     if (routeLine) {
//       rideMap.removeLayer(routeLine);
//       routeLine = null;
//     }
//     document.getElementById("price-output").textContent = "";
//     return;
//   }

//   const coords = await getCoordinates(query);
//   if (!coords) {
//     console.log("Could not find location for:", query);
//     return;
//   }

//   initRideMap();

//   // Remove old drop marker
//   if (dropMarker) rideMap.removeLayer(dropMarker);

//   // Create custom red marker for dropoff
//   const dropIcon = L.divIcon({
//     className: "custom-marker",
//     html: '<div style="background: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
//     iconSize: [30, 30],
//     iconAnchor: [15, 15],
//   });

//   // Add new drop marker
//   dropMarker = L.marker(coords, { icon: dropIcon })
//     .addTo(rideMap)
//     .bindPopup(`<b>🎯 Dropoff</b><br>${query}`)
//     .openPopup();

//   // Update route and price
//   updateRoute();
// }
// 22-10-25
// Update route between pickup and drop
// function updateRoute() {
//   if (!pickupMarker || !dropMarker) return;

//   const pickupCoords = pickupMarker.getLatLng();
//   const dropCoords = dropMarker.getLatLng();

  
//   const apiKey = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijg0MWNjMGU1OGNhYTQzZGFhMjM4NjYzMWY5Y2M1NTM3IiwiaCI6Im11cm11cjY0In0="; // <-- replace this with your key
//   const url = `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${apiKey}&start=${pickupCoords.lng},${pickupCoords.lat}&end=${dropCoords.lng},${dropCoords.lat}`;

//   // Remove old route
//   if (routeLine) rideMap.removeLayer(routeLine);

//   // Draw new route
//   routeLine = L.polyline(
//     [
//       [pickupCoords.lat, pickupCoords.lng],
//       [dropCoords.lat, dropCoords.lng],
//     ],
//     {
//       color: "#3b82f6",
//       weight: 4,
//       opacity: 0.7,
//       dashArray: "10, 5",
//     }
//   ).addTo(rideMap);

//   // Fit map to show both markers
//   rideMap.fitBounds(
//     L.latLngBounds(
//       [pickupCoords.lat, pickupCoords.lng],
//       [dropCoords.lat, dropCoords.lng]
//     ),
//     { padding: [50, 50] }
//   );
// // Update route between pickup and drop using OpenRouteService API



//   // Calculate distance and price
//   const distance = getDistance(
//     [pickupCoords.lat, pickupCoords.lng],
//     [dropCoords.lat, dropCoords.lng]
//   );
//   const price = (distance * 15).toFixed(2); // ₹15 per km

//   const priceOutput = document.getElementById("price-output");
//   if (priceOutput) {
//     priceOutput.innerHTML = `
//       <strong>Distance:</strong> ${distance.toFixed(2)} km<br>
//       <strong>Estimated Price:</strong> ₹${price}
//     `;
//   }
// }
// Update route between pickup and drop using OpenRouteService API
// Update route between pickup and drop using ORS API or fallback straight line
// Update route between pickup and drop using OSRM (Open Source Routing Machine)
// No API key required! 🎉
// Simpler approach: OSRM with CORS proxy fallback
// date*****22-10-25
// async function updateRoute() {
//   if (!pickupMarker || !dropMarker) return;

//   const pickupCoords = pickupMarker.getLatLng();
//   const dropCoords = dropMarker.getLatLng();

//   // Remove old route
//   if (routeLine) rideMap.removeLayer(routeLine);

//   let routeCoords = [];
//   let distanceKm = 0;
//   let durationMinutes = null;
//   let isRoadDistance = false;

//   // Try OSRM with CORS proxy
//   const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${pickupCoords.lng},${pickupCoords.lat};${dropCoords.lng},${dropCoords.lat}?overview=full&geometries=geojson`;
  
//   // Use CORS proxy if direct access fails
//   const corsProxy = "https://corsproxy.io/?";
//   const urlToTry = corsProxy + encodeURIComponent(osrmUrl);

//   try {
//     console.log("🔄 Fetching route...");
//     const response = await fetch(urlToTry, {
//       method: 'GET',
//       headers: {
//         'Accept': 'application/json',
//       }
//     });
    
//     const data = await response.json();
//     console.log("📦 Response:", data);

//     if (data.code === "Ok" && data.routes && data.routes.length > 0) {
//       const route = data.routes[0];
//       routeCoords = route.geometry.coordinates.map(c => [c[1], c[0]]);
//       distanceKm = route.distance / 1000;
//       durationMinutes = Math.round(route.duration / 60);
//       isRoadDistance = true;
      
//       console.log("✅ Got road distance:", distanceKm.toFixed(2), "km");
//     } else {
//       throw new Error("No valid route found");
//     }
//   } catch (err) {
//     console.log("❌ API failed:", err.message, "- Using estimated distance");
    
//     // Fallback: Calculate estimated road distance
//     routeCoords = [
//       [pickupCoords.lat, pickupCoords.lng],
//       [dropCoords.lat, dropCoords.lng]
//     ];
    
//     const straightDistance = getDistance(
//       [pickupCoords.lat, pickupCoords.lng], 
//       [dropCoords.lat, dropCoords.lng]
//     );
    
//     // Estimate road distance (typically 30% longer than straight line)
//     distanceKm = straightDistance * 1.3;
//     isRoadDistance = false;
//   }

//   // Draw route on map
//   routeLine = L.polyline(routeCoords, {
//     color: isRoadDistance ? "#3b82f6" : "#fbbf24",
//     weight: 5,
//     opacity: 0.8,
//     smoothFactor: 1.0,
//   }).addTo(rideMap);

//   // Fit map to show entire route
//   rideMap.fitBounds(routeLine.getBounds(), { padding: [50, 50] });

//   // Calculate price (₹15 per km)
//   const price = (distanceKm * 15).toFixed(2);

//   // Display results
//   const priceOutput = document.getElementById("price-output");
//   if (priceOutput) {
//     let html = `
//       <strong>Distance ${isRoadDistance ? "(by road)" : "(estimated)"}:</strong> ${distanceKm.toFixed(2)} km<br>
//     `;
    
//     if (durationMinutes) {
//       html += `<strong>Estimated Time:</strong> ${durationMinutes} minutes<br>`;
//     }
    
//     html += `<strong>Estimated Price:</strong> ₹${price}`;
    
//     if (!isRoadDistance) {
//       html += `<br><small style="color: #fbbf24;">⚠️ Showing estimated road distance (actual may vary)</small>`;
//     }
    
//     priceOutput.innerHTML = html;
//   }
// }

// // Function to show price & route (triggered by button)
// async function showPrice() {
//   const pickup = document.getElementById("pickup").value.trim();
//   const drop = document.getElementById("dropoff").value.trim();
//   const priceOutput = document.getElementById("price-output");

//   if (!pickup || !drop) {
//     alert("⚠️ Please enter both pickup and dropoff locations.");
//     return;
//   }

//   initRideMap();

//   const pickupCoords = await getCoordinates(pickup);
//   const dropCoords = await getCoordinates(drop);

//   if (!pickupCoords || !dropCoords) {
//     alert("❌ Unable to locate one or both locations. Please try again.");
//     return;
//   }

//   // Clear existing markers/route
//   if (pickupMarker) rideMap.removeLayer(pickupMarker);
//   if (dropMarker) rideMap.removeLayer(dropMarker);
//   if (routeLine) rideMap.removeLayer(routeLine);

//   // Create custom markers
//   const pickupIcon = L.divIcon({
//     className: "custom-marker",
//     html: '<div style="background: #10b981; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
//     iconSize: [30, 30],
//     iconAnchor: [15, 15],
//   });

//   const dropIcon = L.divIcon({
//     className: "custom-marker",
//     html: '<div style="background: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
//     iconSize: [30, 30],
//     iconAnchor: [15, 15],
//   });

//   // Add new markers
//   pickupMarker = L.marker(pickupCoords, { icon: pickupIcon })
//     .addTo(rideMap)
//     .bindPopup(`<b>📍 Pickup</b><br>${pickup}`);

//   dropMarker = L.marker(dropCoords, { icon: dropIcon })
//     .addTo(rideMap)
//     .bindPopup(`<b>🎯 Dropoff</b><br>${drop}`);

//   // Draw route
//   routeLine = L.polyline([pickupCoords, dropCoords], {
//     color: "#3b82f6",
//     weight: 4,
//     opacity: 0.7,
//     dashArray: "10, 5",
//   }).addTo(rideMap);

//   // Zoom to fit both points
//   rideMap.fitBounds(L.latLngBounds([pickupCoords, dropCoords]), {
//     padding: [50, 50],
//   });

//   // Calculate distance and price
//   const distance = getDistance(pickupCoords, dropCoords);
//   const price = (distance * 15).toFixed(2);

//   priceOutput.innerHTML = `
//     <strong>Distance:</strong> ${distance.toFixed(2)} km<br>
//     <strong>Estimated Price:</strong> ₹${price}
//   `;
// }

// // 🧩 Initialize live location updates
// function initLiveLocationUpdate() {
//   const pickupInput = document.getElementById("pickup");
//   const dropoffInput = document.getElementById("dropoff");

//   if (pickupInput) {
//     pickupInput.addEventListener("input", () => {
//       clearTimeout(pickupTimeout);
//       pickupTimeout = setTimeout(() => {
//         const query = pickupInput.value.trim();
//         updatePickupLocation(query);
//       }, 1000); // Wait 1 second after user stops typing
//     });
//   }

//   if (dropoffInput) {
//     dropoffInput.addEventListener("input", () => {
//       clearTimeout(dropoffTimeout);
//       dropoffTimeout = setTimeout(() => {
//         const query = dropoffInput.value.trim();
//         updateDropoffLocation(query);
//       }, 1000);
//     });
//   }
// }

// // Initialize when DOM is ready
// if (document.readyState === "loading") {
//   document.addEventListener("DOMContentLoaded", initLiveLocationUpdate);
// } else {
//   initLiveLocationUpdate();
// }

// // Call this whenever the ride page becomes visible
// function showRidePage() {
//   // Your existing code to show the page
//   document.getElementById('ride-page').style.display = 'block';
  
//   // If map already exists, refresh it
//   if (rideMap) {
//     setTimeout(() => {
//       rideMap.invalidateSize();
//     }, 100);
//   }
// }

  let rideMap, pickupMarker, dropMarker, routeControl;
    let pickupTimeout = null;
    let dropoffTimeout = null;

    // Initialize map when ride page loads
    function initRideMap() {
      if (!rideMap) {
        rideMap = L.map("map-container").setView([18.5204, 73.8567], 12);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution: "&copy; OpenStreetMap contributors",
        }).addTo(rideMap);
      }
    }

    // Convert place name → coordinates using OpenStreetMap Nominatim
    async function getCoordinates(location) {
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
            location
          )}&limit=1`,
          {
            headers: {
              "User-Agent": "RideShareApp/1.0",
            },
          }
        );
        const data = await response.json();
        if (data.length > 0) {
          return [parseFloat(data[0].lat), parseFloat(data[0].lon)];
        }
        return null;
      } catch (err) {
        console.error("Error fetching coordinates:", err);
        return null;
      }
    }

    // 🧠 Live pickup marker update
    async function updatePickupLocation(query) {
      if (!query || query.trim() === "") {
        if (pickupMarker) {
          rideMap.removeLayer(pickupMarker);
          pickupMarker = null;
          if (routeControl) {
            rideMap.removeControl(routeControl);
            routeControl = null;
          }
        }
        return;
      }

      const coords = await getCoordinates(query);
      if (!coords) {
        console.log("Could not find location for:", query);
        return;
      }

      initRideMap();

      if (pickupMarker) rideMap.removeLayer(pickupMarker);

      const pickupIcon = L.divIcon({
        className: "custom-marker",
        html: '<div style="background: #10b981; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      pickupMarker = L.marker(coords, { icon: pickupIcon })
        .addTo(rideMap)
        .bindPopup(`<b>📍 Pickup</b><br>${query}`)
        .openPopup();

      rideMap.setView(coords, 14);
      updateRoute();
    }

    // 🧠 Live dropoff marker update
    async function updateDropoffLocation(query) {
      if (!query || query.trim() === "") {
        if (dropMarker) {
          rideMap.removeLayer(dropMarker);
          dropMarker = null;
        }
        if (routeControl) {
          rideMap.removeControl(routeControl);
          routeControl = null;
        }
        document.getElementById("price-output").textContent = "";
        return;
      }

      const coords = await getCoordinates(query);
      if (!coords) {
        console.log("Could not find location for:", query);
        return;
      }

      initRideMap();

      if (dropMarker) rideMap.removeLayer(dropMarker);

      const dropIcon = L.divIcon({
        className: "custom-marker",
        html: '<div style="background: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      dropMarker = L.marker(coords, { icon: dropIcon })
        .addTo(rideMap)
        .bindPopup(`<b>🎯 Dropoff</b><br>${query}`)
        .openPopup();

      updateRoute();
    }

    // 🛣️ Update route with ACTUAL ROAD PATH (not straight line!)
    async function updateRoute() {
      if (!pickupMarker || !dropMarker) return;

      const pickupCoords = pickupMarker.getLatLng();
      const dropCoords = dropMarker.getLatLng();

      // Remove old route control if exists
      if (routeControl) {
        rideMap.removeControl(routeControl);
      }

      // Create route using Leaflet Routing Machine with OSRM
      routeControl = L.Routing.control({
        waypoints: [
          L.latLng(pickupCoords.lat, pickupCoords.lng),
          L.latLng(dropCoords.lat, dropCoords.lng)
        ],
        routeWhileDragging: false,
        show: false,
        addWaypoints: false,
        router: L.Routing.osrmv1({
          serviceUrl: 'https://router.project-osrm.org/route/v1'
        }),
        lineOptions: {
          styles: [
            { 
              color: '#3b82f6', 
              opacity: 0.8, 
              weight: 6 
            }
          ]
        },
        createMarker: function() { 
          return null; 
        }
      }).addTo(rideMap);

      // When route is calculated, display distance and price
      routeControl.on('routesfound', function(e) {
        const routes = e.routes;
        const route = routes[0];

        // Get actual road distance in kilometers
        const distanceKm = (route.summary.totalDistance / 1000).toFixed(2);
        const durationMin = Math.round(route.summary.totalTime / 60);
        const price = (distanceKm * 15).toFixed(2);

        const priceOutput = document.getElementById("price-output");
        if (priceOutput) {
          priceOutput.innerHTML = `\n            <strong>Distance (by road):</strong> ${distanceKm} km<br>\n            <strong>Estimated Time:</strong> ${durationMin} minutes<br>\n            <strong>Estimated Price:</strong> ₹${price}\n            <div style="margin-top: 8px; padding: 6px; background: #10b98120; border-left: 3px solid #10b981; font-size: 12px;">\n              ✅ <em>Route follows actual roads</em>\n            </div>\n          `;
        }

        console.log("✅ Road route calculated!");
        console.log("📏 Distance:", distanceKm, "km");
        console.log("⏱️ Duration:", durationMin, "minutes");
      });

      // Handle errors
      routeControl.on('routingerror', function(e) {
        console.error('❌ Routing error:', e.error);

        const priceOutput = document.getElementById("price-output");
        if (priceOutput) {
          priceOutput.innerHTML = `\n            <div style="color: #ef4444;">\n              ⚠️ Unable to calculate road route. Please try again or check your internet connection.\n            </div>\n          `;
        }
      });
    }

    // Function to show price & route (triggered by button)
    async function showPrice() {
      const pickup = document.getElementById("pickup").value.trim();
      const drop = document.getElementById("dropoff").value.trim();

      if (!pickup || !drop) {
        alert("⚠️ Please enter both pickup and dropoff locations.");
        return;
      }

      initRideMap();

      const pickupCoords = await getCoordinates(pickup);
      const dropCoords = await getCoordinates(drop);

      if (!pickupCoords || !dropCoords) {
        alert("❌ Unable to locate one or both locations. Please try again.");
        return;
      }

      // Clear existing markers
      if (pickupMarker) rideMap.removeLayer(pickupMarker);
      if (dropMarker) rideMap.removeLayer(dropMarker);
      if (routeControl) rideMap.removeControl(routeControl);

      const pickupIcon = L.divIcon({
        className: "custom-marker",
        html: '<div style="background: #10b981; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      const dropIcon = L.divIcon({
        className: "custom-marker",
        html: '<div style="background: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      pickupMarker = L.marker(pickupCoords, { icon: pickupIcon })
        .addTo(rideMap)
        .bindPopup(`<b>📍 Pickup</b><br>${pickup}`);

      dropMarker = L.marker(dropCoords, { icon: dropIcon })
        .addTo(rideMap)
        .bindPopup(`<b>🎯 Dropoff</b><br>${drop}`);

      updateRoute();
    }

    // 🧩 Initialize live location updates
    function initLiveLocationUpdate() {
      const pickupInput = document.getElementById("pickup");
      const dropoffInput = document.getElementById("dropoff");

      if (pickupInput) {
        pickupInput.addEventListener("input", () => {
          clearTimeout(pickupTimeout);
          pickupTimeout = setTimeout(() => {
            const query = pickupInput.value.trim();
            updatePickupLocation(query);
          }, 1000);
        });
      }

      if (dropoffInput) {
        dropoffInput.addEventListener("input", () => {
          clearTimeout(dropoffTimeout);
          dropoffTimeout = setTimeout(() => {
            const query = dropoffInput.value.trim();
            updateDropoffLocation(query);
          }, 1000);
        });
      }
    }

    // Initialize when DOM is ready
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initLiveLocationUpdate);
    } else {
      initLiveLocationUpdate();
    }

    // Call this whenever the ride page becomes visible
    function showRidePage() {
      document.getElementById('ride-page').style.display = 'block';
      
      if (rideMap) {
        setTimeout(() => {
          rideMap.invalidateSize();
        }, 100);
      }
    }
