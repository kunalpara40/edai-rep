(function () {
  'use strict';

  /* ---------- Page navigation & footer ---------- */
  // function showPage(pageId) {
  //   console.log('showPage called with:', pageId); // Debug log
    
  //   // hide all pages (use display:block/none for robustness)
  //   document.querySelectorAll('.page-container').forEach(p => {
  //     p.style.display = 'none';
  //     p.classList.remove('active');
  //   });

  //   const target = document.getElementById(pageId + '-page');
  //   console.log('Target element:', target); // Debug log
    
  //   if (target) {
  //     target.style.display = 'block';
  //     target.classList.add('active');
      
  //     // Initialize map when ride page is displayed
  //     if (pageId === 'ride') {
  //       setTimeout(() => {
  //         if (typeof initRideMap === 'function') {
  //           initRideMap("map-container");
  //         }
  //       }, 100);
  //     }
  //   } else {
  //     console.error('Page not found:', pageId + '-page');
  //   }

  //   // footer toggle
  //   const footer = document.getElementById('main-footer');
  //   if (footer) footer.style.display = (pageId === 'ride' || pageId === 'driver-login') ? 'none' : 'block';

  //   // update nav-link active class (if nav links exist)
  //   document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
  //   const navLinks = Array.from(document.querySelectorAll('.nav-link'));
  //   const found = navLinks.find(link => link.getAttribute('onclick')?.includes(pageId) ||
  //     (link.textContent && link.textContent.trim().toLowerCase().includes(pageId)));
  //   if (found) found.classList.add('active');
  // }

  // // ⭐ EXPOSE showPage globally so HTML onclick can access it
  // window.showPage = showPage;

  // // default page: home
  // document.addEventListener('DOMContentLoaded', function() {
  //   if (!document.querySelector('.page-container.active')) {
  //     showPage('home');
  //   }
  // });



  // Replace your showPage function with this fixed version
// Put this at the TOP of your index.js file

(function () {
  'use strict';

  /* ---------- Page navigation & footer ---------- */
  // function showPage(pageId) {
  //   console.log('🔍 showPage called with:', pageId); // Debug log
    
  //   // Hide all pages
  //   const allPages = document.querySelectorAll('.page-container');
  //   console.log('📄 Total pages found:', allPages.length);
    
  //   allPages.forEach(p => {
  //     p.style.display = 'none';
  //     p.classList.remove('active');
  //     console.log('  Hidden:', p.id);
  //   });

   
  //   const targetId = pageId + '-page';
  //   const target = document.getElementById(targetId);
    
  //   console.log('🎯 Looking for page:', targetId);
  //   console.log('🎯 Found element:', target);
    
  //   if (target) {
  //     target.style.display = 'block';
  //     target.classList.add('active');
  //     console.log('✅ Showing page:', targetId);
      
    
  //     if (pageId === 'ride') {
  //       setTimeout(() => {
  //         if (typeof initRideMap === 'function') {
  //           initRideMap("ride-map-container");
  //         }
  //       }, 100);
  //     }
  //   } else {
  //     console.error('❌ Page not found:', targetId);
  //     console.log('Available page IDs:');
  //     allPages.forEach(p => console.log('  -', p.id));
  //   }

   
  //   const footer = document.getElementById('main-footer');
  //   if (footer) {
  //     footer.style.display = (pageId === 'ride' || pageId === 'driver-login') ? 'none' : 'block';
  //   }

    
  //   document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
  //   const navLinks = Array.from(document.querySelectorAll('.nav-link'));
  //   const found = navLinks.find(link => {
  //     const onclick = link.getAttribute('onclick');
  //     return onclick && onclick.includes(pageId);
  //   });
  //   if (found) found.classList.add('active');
  // }

 
  // window.showPage = showPage;

  // document.addEventListener('DOMContentLoaded', function() {
  //   console.log('🚀 DOM loaded, initializing pages...');
    
   
  //   const allPages = document.querySelectorAll('.page-container');
  //   console.log('📋 Available pages:');
  //   allPages.forEach(p => {
  //     console.log('  - ' + p.id + (p.classList.contains('active') ? ' (active)' : ''));
  //   });
    
    
  //   if (!document.querySelector('.page-container.active')) {
  //     console.log('No active page found, showing home');
  //     showPage('home');
  //   }
  // });


  // Add this IMPROVED showPage function at the top of your index.js
// This replaces your existing showPage function

function showPage(pageId) {
  console.log('🔍 showPage called with:', pageId);
  
  // Get all page containers
  const allPages = document.querySelectorAll('.page-container');
  console.log('📄 Total pages found:', allPages.length);
  
  // Hide all pages first
  allPages.forEach(page => {
    page.style.display = 'none';
    page.classList.remove('active');
    console.log('  Hidden:', page.id);
  });

  // Show the target page
  const targetId = pageId + '-page';
  const targetPage = document.getElementById(targetId);
  
  console.log('🎯 Looking for:', targetId);
  console.log('🎯 Found element:', targetPage);
  
  if (targetPage) {
    // Force display and active class
    targetPage.style.display = 'flex';
    targetPage.classList.add('active');
    
    // Force all children to be visible
    targetPage.style.opacity = '1';
    targetPage.style.visibility = 'visible';
    
    console.log('✅ Showing page:', targetId);
    
    // Special handling for pages with maps
    if (pageId === 'ride') {
      setTimeout(() => {
        if (typeof initRideMap === 'function') {
          initRideMap("ride-map-container");
        }
      }, 100);
    }
    
    // Special handling for driver login
    if (pageId === 'driver-login') {
      console.log('🚗 Driver login page activated');
      const mainContainer = targetPage.querySelector('.main-container');
      if (mainContainer) {
        mainContainer.style.display = 'flex';
        mainContainer.style.opacity = '1';
        mainContainer.style.visibility = 'visible';
        console.log('✅ Main container forced visible');
      }
    }
  } else {
    console.error('❌ Page not found:', targetId);
    console.log('Available pages:');
    allPages.forEach(p => console.log('  -', p.id));
  }

  // Handle footer visibility
  const footer = document.getElementById('main-footer');
  if (footer) {
    footer.style.display = (pageId === 'ride' || pageId === 'driver-login') ? 'none' : 'block';
  }

  // Update navigation active states
  document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
  const navLinks = Array.from(document.querySelectorAll('.nav-link'));
  const activeLink = navLinks.find(link => {
    const onclick = link.getAttribute('onclick');
    return onclick && onclick.includes(pageId);
  });
  if (activeLink) activeLink.classList.add('active');
}

// Make sure showPage is globally accessible
window.showPage = showPage;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 DOM loaded, initializing pages...');
  
  // List all available pages
  const allPages = document.querySelectorAll('.page-container');
  console.log('📋 Available pages:');
  allPages.forEach(p => {
    console.log('  - ' + p.id + (p.classList.contains('active') ? ' (active)' : ''));
  });
  
  // Show home page if no page is active
  if (!document.querySelector('.page-container.active')) {
    console.log('No active page found, showing home');
    showPage('home');
  }
});
  // Rest of your code...
})();

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
    if (window.scrollY > 50) navbar.classList.add('scrolled'); 
    else navbar.classList.remove('scrolled');
  });

  /* ---------- Theme toggle ---------- */
  window.toggleTheme = function () {
    document.body.classList.toggle('dark-mode');
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    btn.textContent = document.body.classList.contains('dark-mode') ? '💡' : '🔆';
  };

  /* ---------- Form step controls ---------- */
  // function showStep(stepNumber) {
  //   document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
  //   const el = document.getElementById('step' + stepNumber);
  //   if (el) el.classList.add('active');

  //   document.querySelectorAll('.progress-step').forEach((step, idx) => {
  //     step.classList.remove('active', 'completed');
  //     if (idx + 1 < stepNumber) step.classList.add('completed');
  //     else if (idx + 1 === stepNumber) step.classList.add('active');
  //   });
  // }
  // window.showStep = showStep;

  // function nextStep(currentStep) {
  //   let valid = true;
  //   // Step 1
  //   if (currentStep === 1) {
  //     const firstName = (document.getElementById('firstName') || {}).value?.trim();
  //     const lastName = (document.getElementById('lastName') || {}).value?.trim();
  //     const email = (document.getElementById('email') || {}).value?.trim();
  //     const phone = (document.getElementById('phone') || {}).value?.trim();
  //     const phoneError = document.getElementById('phoneError');
  //     if (!firstName || !lastName || !email || !phone) {
  //       alert('Please fill all required fields in Step 1');
  //       valid = false;
  //     } else if (!/^\d{10}$/.test(phone)) {
  //       if (phoneError) phoneError.style.display = 'block';
  //       valid = false;
  //     } else if (phoneError) phoneError.style.display = 'none';
  //   }
  //   // Step 2
  //   if (currentStep === 2) {
  //     const password = (document.getElementById('password') || {}).value;
  //     const confirmPassword = (document.getElementById('confirmPassword') || {}).value;
  //     if (!password || !confirmPassword) {
  //       alert('Please fill all required fields in Step 2');
  //       valid = false;
  //     } else if (password !== confirmPassword) {
  //       alert('Passwords do not match');
  //       valid = false;
  //     }
  //   }
  //   if (valid) showStep(currentStep + 1);
  // }
  // window.nextStep = nextStep;

/* showStep: show requested step and update progress dots */
function showStep(stepNumber) {
  // Use the driver sign-up page container to determine scope
  const driverPage = document.getElementById('driver-signup-page');
  const isDriver = !!driverPage && driverPage.classList.contains('active');

  const stepPrefix = isDriver ? 'driverStep' : 'step';
  const container = isDriver ? driverPage : document;

  // Hide all steps, then show the requested
  container.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
  const currentStep = document.getElementById(stepPrefix + stepNumber);
  if (currentStep) currentStep.classList.add('active');

  // Update progress bar
  const progress = container.querySelectorAll('.progress-step');
  progress.forEach((dot, idx) => {
    dot.classList.remove('active', 'completed');
    if (idx + 1 < stepNumber) dot.classList.add('completed');
    else if (idx + 1 === stepNumber) dot.classList.add('active');
  });
}
window.showStep = showStep;

/* nextStep: validates current step and either navigates or submits at final step */
async function nextStep(currentStep) {
  let valid = true;

  // Check if we are in driver signup UI by driver-signup-page presence & active
  const driverPage = document.getElementById('driver-signup-page');
  const isDriver = !!driverPage && driverPage.classList.contains('active');

  if (isDriver) {
    // ---- DRIVER SIGNUP steps mapping (HTML): step1 = personal, step2 = license, step3 = account/security
    if (currentStep === 1) {
      const firstName = (document.getElementById('driver_firstName') || {}).value?.trim();
      const lastName = (document.getElementById('driver_lastName') || {}).value?.trim();
      const email = (document.getElementById('driver_email') || {}).value?.trim();
      const phone = (document.getElementById('driver_phone') || {}).value?.trim();

      if (!(firstName && lastName) || !email || !phone) {
        alert('Please fill all required fields in Step 1 (name, email, phone).');
        valid = false;
      } else if (!/^\d{10}$/.test(phone)) {
        alert('Please enter a valid 10-digit phone number (digits only).');
        valid = false;
      }
    }

    if (currentStep === 2) {
      const licenseNo = (document.getElementById('license_no') || {}).value?.trim();
      const licenseFileEl = document.getElementById('license_image');
      const licenseFile = licenseFileEl && licenseFileEl.files && licenseFileEl.files[0];
      const vehicleType = (document.getElementById('vehicle_type') || {}).value;

      if (!licenseNo || !licenseFile || !vehicleType) {
        alert('Please enter license number, upload license image and select vehicle type.');
        valid = false;
      } else {
        // file checks
        const max = 5 * 1024 * 1024; // 5 MB
        if (licenseFile.size > max) {
          alert('License file must be 5 MB or smaller.');
          valid = false;
        }
        const ext = licenseFile.name.split('.').pop().toLowerCase();
        if (!['png','jpg','jpeg','pdf'].includes(ext)) {
          alert('Allowed license file types: png, jpg, jpeg, pdf');
          valid = false;
        }
      }
    }

    if (currentStep === 3) {
      // final step: password & confirm
      const password = (document.getElementById('password_driver') || {}).value || '';
      const confirmPassword = (document.getElementById('confirmPassword_driver') || {}).value || '';
      if (!password || !confirmPassword) {
        alert('Please fill password and confirm password.');
        valid = false;
      } else if (password.length < 8) {
        alert('Password must be at least 8 characters.');
        valid = false;
      } else if (password !== confirmPassword) {
        alert('Passwords do not match.');
        valid = false;
      }
    }

    if (!valid) return;

    // If currentStep < 3, just move to next step. If currentStep === 3, submit the driver signup.
    if (currentStep < 3) {
      showStep(currentStep + 1);
      return;
    } else {
      // currentStep === 3 -> submit
      await submitDriverForm();
      return;
    }
  }

  // ---------- Non-driver (user) flow preserved below (unchanged) ----------
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

  if (valid) showStep(currentStep + 1);
}
window.nextStep = nextStep;

/* ---------- submitDriverForm: gathers all inputs and posts to /driver/signup ---------- */
/* Replace your submitDriverForm function with this updated version */
async function submitDriverForm() {
  // Collect driver inputs
  const firstName = (document.getElementById('driver_firstName') || {}).value?.trim() || '';
  const lastName = (document.getElementById('driver_lastName') || {}).value?.trim() || '';
  const full_name = `${firstName} ${lastName}`.trim();
  
  const email = (document.getElementById('driver_email') || {}).value?.trim() || '';
  const phone = (document.getElementById('driver_phone') || {}).value?.trim() || '';
  const license_no = (document.getElementById('license_no') || {}).value?.trim() || '';
  const vehicle_type = (document.getElementById('vehicle_type') || {}).value || '';
  
  // NEW: Collect vehicle make, model, and license plate
  const vehicle_make = (document.getElementById('vehicle_make') || {}).value?.trim() || '';
  const vehicle_model = (document.getElementById('vehicle_model') || {}).value?.trim() || '';
  const license_plate = (document.getElementById('license_plate') || {}).value?.trim() || '';
  
  const password = (document.getElementById('password_driver') || {}).value || '';
  const licenseFileEl = document.getElementById('license_image');
  const licenseFile = licenseFileEl && licenseFileEl.files && licenseFileEl.files[0];
  
  if (!full_name) {
    alert('Please enter your first and last name');
    return;
  }

  console.log('🚀 Driver signup - Collecting form data...');
  console.log('📋 Form data:');
  console.log('  firstName:', firstName);
  console.log('  lastName:', lastName);
  console.log('  full_name:', full_name);
  console.log('  phone:', phone);
  console.log('  email:', email);
  console.log('  license_no:', license_no);
  console.log('  vehicle_type:', vehicle_type);
  console.log('  vehicle_make:', vehicle_make);
  console.log('  vehicle_model:', vehicle_model);
  console.log('  license_plate:', license_plate);
  console.log('  password length:', password.length);
  console.log('  license file:', licenseFile ? licenseFile.name : 'none');

  // Build FormData for multipart upload
  const fd = new FormData();
  fd.append('full_name', full_name);
  fd.append('firstName', firstName);
  fd.append('lastName', lastName);
  fd.append('email', email);
  fd.append('phone', phone);
  fd.append('license_no', license_no);
  fd.append('vehicle_type', vehicle_type);
  fd.append('vehicle_make', vehicle_make);      // NEW
  fd.append('vehicle_model', vehicle_model);    // NEW
  fd.append('license_plate', license_plate);    // NEW
  fd.append('password', password);

  if (licenseFile) {
    fd.append('license_image', licenseFile, licenseFile.name);
  }

  try {
    const submitBtn = document.querySelector('#driverStep3 button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.dataset.oldText = submitBtn.innerText;
      submitBtn.innerText = 'Creating account...';
    }

    console.log('🌐 Sending POST to /driver/signup...');

    const res = await fetch('/driver/signup', {
      method: 'POST',
      body: fd,
      credentials: 'same-origin'
    });

    console.log('📥 Response status:', res.status);

    const data = await res.json().catch(() => ({}));
    console.log('📥 Response data:', data);

    if (res.ok) {
      alert(data.message || 'Driver registered successfully!');
      // Redirect to driver login
      window.location.href = '/driver/login';
    } else {
      // Server error or validation failed
      alert('Signup failed: ' + (data.error || JSON.stringify(data) || res.statusText));
    }
  } catch (err) {
    console.error('❌ submitDriverForm error:', err);
    alert('Network or server error. Check Flask console for details.');
  } finally {
    const submitBtn = document.querySelector('#driverStep3 button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerText = submitBtn.dataset.oldText || 'Create Driver Account';
    }
  }
}

  /* ---------- Animations for inputs / containers ---------- */
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

  /* ---------- Auth Handlers ---------- */
  function initAuthHandlers() {
    // Login handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value;

        try {
          const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password })
          });

          if (res.ok) {
            window.location.href = '/';
          } else {
            const json = await res.json().catch(() => ({}));
            alert(json.error || 'Login failed');
          }
        } catch (err) {
          console.error('Login error:', err);
          alert('Network error. Please check your connection.');
        }
      });
    }

    // Driver login handler
    const driverLoginForm = document.getElementById('driver-login-form');
    if (driverLoginForm) {
      driverLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const phoneElem = document.getElementById('driver-login-phone');
        const emailElem = document.getElementById('driver-login-email');
        const passwordElem = document.getElementById('driver-login-password');

        const phone = phoneElem ? phoneElem.value.trim() : '';
        const email = emailElem ? emailElem.value.trim() : '';
        const password = passwordElem ? passwordElem.value : '';

        if (!password || (!phone && !email)) {
          alert('Enter phone or email, and password');
          return;
        }

        // prefer phone if provided
        const payload = phone ? { phone, password } : { email, password };

        try {
          const res = await fetch('/driver/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(payload)
          });

          const json = await res.json().catch(()=>({}));

          if (res.ok) {
            // small delay to allow cookie/session to be established
            setTimeout(() => { window.location.href = json.redirect || '/driver/dashboard'; }, 300);
          } else {
            alert(json.error || 'Login failed');
          }
        } catch (err) {
          console.error('Driver login error:', err);
          alert('Network error. Please check your connection.');
        }
      });
    }

    // Signup handler (user) - existing
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

        if (!/^\d{10}$/.test(userData.phone)) {
          alert('Please enter valid 10-digit phone');
          return;
        }

        try {
          const res = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(userData)
          });
          
          const json = await res.json().catch(() => ({}));
          
          if (res.status === 409) {
            alert(json.error || 'Email exists. Please login.');
            return;
          }
          
          if (!res.ok) {
            alert(json.error || 'Signup failed');
            return;
          }

          alert(json.message || 'Account created!');
          showPage('login');
        } catch (err) {
          console.error('Signup error:', err);
          alert('Network error. Please check your connection.');
        }
      });
    }

  

// User dropdown toggle
const userBtn = document.getElementById("userBtn");
const dropdown = document.querySelector(".user-dropdown");

if (userBtn && dropdown) {
  userBtn.addEventListener("click", (event) => {
    event.stopPropagation();
    dropdown.classList.toggle("open");
  });

  // Close dropdown when clicking outside
  window.addEventListener("click", () => {
    dropdown.classList.remove("open");
  });
}

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
        window.location.href = '/';
      } else {
        console.error('Logout failed');
      }
    } catch (err) {
      console.error('Logout failed:', err);
    }
  });
}
// yaha se
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
          const opt = document.createElement('option');
          opt.value = c;
          opt.textContent = c;
          citySel.appendChild(opt);
        });
      }
    });
  }

  /* ---------- Init on DOM ready ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM loaded, initializing...'); // Debug log
    
    initAnimations();
    initAuthHandlers();
    initPhoneValidation();
    initStateCity();

    // Hook password strength & confirm listeners
    const pw = document.getElementById('password');
    if (pw) pw.addEventListener('input', checkPasswordStrength);
    
    const cpw = document.getElementById('confirmPassword');
    if (cpw) cpw.addEventListener('input', validatePasswordMatch);

    // also wire driver password fields (if present)
    const dpw = document.getElementById('password_driver');
    const dcpw = document.getElementById('confirmPassword_driver');
    if (dpw) dpw.addEventListener('input', () => {
      // optional: reuse checkPasswordStrength by temporarily mapping ids — skipping for simplicity
    });
    if (dcpw) dcpw.addEventListener('input', () => {
      const pm = document.getElementById('passwordMatch');
      if (!pm) return;
      pm.style.display = (dcpw.value && (dpw && dpw.value !== dcpw.value)) ? 'block' : 'none';
    });
  });

})();

// Call this whenever the ride page becomes visible
function showRidePage() {
  document.getElementById('ride-page').style.display = 'block';
  
  // Initialize map for ride page
  setTimeout(() => {
    initRideMap("ride-map-container");
  }, 100);
}

  let rideMap, pickupMarker, dropMarker, routeControl;
    let pickupTimeout = null;
    let dropoffTimeout = null;

    // Initialize map when ride page loads
    function initRideMap(containerId = "map-container") {
      // Always create a new map instance to avoid conflicts
      if (rideMap) {
        try {
          rideMap.remove();
        } catch (e) {
          console.log("Error removing map:", e);
        }
        rideMap = null;
      }
      
      // Create new map for the specified container
      const container = document.getElementById(containerId);
      if (container) {
        rideMap = L.map(containerId).setView([18.5204, 73.8567], 12);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution: "&copy; OpenStreetMap contributors",
        }).addTo(rideMap);
        
        // Ensure map resizes properly
        setTimeout(() => {
          if (rideMap) {
            try {
              rideMap.invalidateSize();
            } catch (e) {
              console.log("Error invalidating map size:", e);
            }
          }
        }, 100);
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
    async function updatePickupLocation(query, containerId = "map-container") {
      if (!query || query.trim() === "") {
        // Initialize map to clear any existing markers
        initRideMap(containerId);
        
        if (pickupMarker && rideMap) {
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

      initRideMap(containerId);

      // Remove existing pickup marker if it exists
      if (pickupMarker && rideMap) {
        try {
          rideMap.removeLayer(pickupMarker);
        } catch (e) {
          console.log("Error removing pickup marker:", e);
        }
        pickupMarker = null;
      }

      const pickupIcon = L.divIcon({
        className: "custom-marker",
        html: '<div style="background: #10b981; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      if (rideMap) {
        pickupMarker = L.marker(coords, { icon: pickupIcon })
          .addTo(rideMap)
          .bindPopup(`<b>📍 Pickup</b><br>${query}`)
          .openPopup();

        rideMap.setView(coords, 14);
        updateRoute();
      }
    }

    // 🧠 Live dropoff marker update
    async function updateDropoffLocation(query, containerId = "map-container") {
      if (!query || query.trim() === "") {
        // Initialize map to clear any existing markers
        initRideMap(containerId);
        
        if (dropMarker && rideMap) {
          rideMap.removeLayer(dropMarker);
          dropMarker = null;
        }
        if (routeControl && rideMap) {
          rideMap.removeControl(routeControl);
          routeControl = null;
        }
        const priceOutputId = containerId === "ride-map-container" ? "ride-price-output" : "price-output";
        const priceOutput = document.getElementById(priceOutputId);
        if (priceOutput) priceOutput.textContent = "";
        return;
      }

      const coords = await getCoordinates(query);
      if (!coords) {
        console.log("Could not find location for:", query);
        return;
      }

      initRideMap(containerId);

      // Remove existing drop marker if it exists
      if (dropMarker && rideMap) {
        try {
          rideMap.removeLayer(dropMarker);
        } catch (e) {
          console.log("Error removing drop marker:", e);
        }
        dropMarker = null;
      }

      const dropIcon = L.divIcon({
        className: "custom-marker",
        html: '<div style="background: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      if (rideMap) {
        dropMarker = L.marker(coords, { icon: dropIcon })
          .addTo(rideMap)
          .bindPopup(`<b>🎯 Dropoff</b><br>${query}`)
          .openPopup();

        updateRoute();
      }
    }

    // 🛣️ Update route with ACTUAL ROAD PATH (not straight line!)
    async function updateRoute() {
      if (!pickupMarker || !dropMarker || !rideMap) return;

      const pickupCoords = pickupMarker.getLatLng();
      const dropCoords = dropMarker.getLatLng();

      // Remove old route control if exists
      if (routeControl) {
        try {
          rideMap.removeControl(routeControl);
        } catch (e) {
          console.log("Error removing route control:", e);
        }
        routeControl = null;
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

        // Determine which price output to use based on current map
        const containerId = rideMap._container.id;
        const priceOutputId = containerId === "ride-map-container" ? "ride-price-output" : "price-output";
        const priceOutput = document.getElementById(priceOutputId);
        
        if (priceOutput) {
          priceOutput.innerHTML = `
            <strong>Distance (by road):</strong> ${distanceKm} km<br>
            <strong>Estimated Time:</strong> ${durationMin} minutes<br>
            <strong>Estimated Price:</strong> ₹${price}
            <div style="margin-top: 8px; padding: 6px; background: #10b98120; border-left: 3px solid #10b981; font-size: 12px;">
              ✅ <em>Route follows actual roads</em>
            </div>
          `;
        }

        console.log("✅ Road route calculated!");
        console.log("📏 Distance:", distanceKm, "km");
        console.log("⏱️ Duration:", durationMin, "minutes");
      });

      // Handle errors
      routeControl.on('routingerror', function(e) {
        console.error('❌ Routing error:', e.error);

        // Determine which price output to use based on current map
        const containerId = rideMap._container.id;
        const priceOutputId = containerId === "ride-map-container" ? "ride-price-output" : "price-output";
        const priceOutput = document.getElementById(priceOutputId);
        
        if (priceOutput) {
          priceOutput.innerHTML = `
            <div style="color: #ef4444;">
              ⚠️ Unable to calculate road route. Please try again or check your internet connection.
            </div>
          `;
        }
      });
    }

    // Function to show price & route (triggered by button)
    async function showPrice() {
      // Determine which form we're working with based on which button was clicked
      const clickedButton = event && event.target ? event.target : null;
      const isRidePage = clickedButton ? clickedButton.closest('#ride-page') !== null : false;
      
      // Get the appropriate input elements
      const pickupInputId = isRidePage ? "ride-pickup" : "pickup";
      const dropoffInputId = isRidePage ? "ride-dropoff" : "dropoff";
      const containerId = isRidePage ? "ride-map-container" : "map-container";
      
      const pickup = document.getElementById(pickupInputId).value.trim();
      const drop = document.getElementById(dropoffInputId).value.trim();

      if (!pickup || !drop) {
        alert("⚠️ Please enter both pickup and dropoff locations.");
        return;
      }

      initRideMap(containerId);

      const pickupCoords = await getCoordinates(pickup);
      const dropCoords = await getCoordinates(drop);

      if (!pickupCoords || !dropCoords) {
        alert("❌ Unable to locate one or both locations. Please try again.");
        return;
      }

      // Clear existing markers
      if (pickupMarker && rideMap) {
        try {
          rideMap.removeLayer(pickupMarker);
        } catch (e) {
          console.log("Error removing pickup marker:", e);
        }
        pickupMarker = null;
      }
      
      if (dropMarker && rideMap) {
        try {
          rideMap.removeLayer(dropMarker);
        } catch (e) {
          console.log("Error removing drop marker:", e);
        }
        dropMarker = null;
      }
      
      if (routeControl && rideMap) {
        try {
          rideMap.removeControl(routeControl);
        } catch (e) {
          console.log("Error removing route control:", e);
        }
        routeControl = null;
      }

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

      if (rideMap) {
        pickupMarker = L.marker(pickupCoords, { icon: pickupIcon })
          .addTo(rideMap)
          .bindPopup(`<b>📍 Pickup</b><br>${pickup}`);

        dropMarker = L.marker(dropCoords, { icon: dropIcon })
          .addTo(rideMap)
          .bindPopup(`<b>🎯 Dropoff</b><br>${drop}`);

        updateRoute();
      }
    }

    // 🧩 Initialize live location updates
    function initLiveLocationUpdate() {
      // Home page inputs
      const pickupInput = document.getElementById("pickup");
      const dropoffInput = document.getElementById("dropoff");
      
      // Ride page inputs
      const ridePickupInput = document.getElementById("ride-pickup");
      const rideDropoffInput = document.getElementById("ride-dropoff");

      if (pickupInput) {
        pickupInput.addEventListener("input", () => {
          clearTimeout(pickupTimeout);
          pickupTimeout = setTimeout(() => {
            const query = pickupInput.value.trim();
            updatePickupLocation(query, "map-container");
          }, 1000);
        });
      }

      if (dropoffInput) {
        dropoffInput.addEventListener("input", () => {
          clearTimeout(dropoffTimeout);
          dropoffTimeout = setTimeout(() => {
            const query = dropoffInput.value.trim();
            updateDropoffLocation(query, "map-container");
          }, 1000);
        });
      }
      
      if (ridePickupInput) {
        ridePickupInput.addEventListener("input", () => {
          clearTimeout(pickupTimeout);
          pickupTimeout = setTimeout(() => {
            const query = ridePickupInput.value.trim();
            updatePickupLocation(query, "ride-map-container");
          }, 1000);
        });
      }

      if (rideDropoffInput) {
        rideDropoffInput.addEventListener("input", () => {
          clearTimeout(dropoffTimeout);
          dropoffTimeout = setTimeout(() => {
            const query = rideDropoffInput.value.trim();
            updateDropoffLocation(query, "ride-map-container");
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
      
      // Initialize map for ride page
      initRideMap("ride-map-container");
    }

   