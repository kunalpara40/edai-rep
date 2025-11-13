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

 // Add this to your index.js file or replace the existing map initialization

let rideMap, pickupMarker, dropMarker, routeControl;
let pickupTimeout = null;
let dropoffTimeout = null;
let userCurrentLocation = null;


function initRideMap(containerId = "map-container") {
  if (rideMap) {
    try {
      rideMap.remove();
    } catch (e) {
      console.log("Error removing map:", e);
    }
    rideMap = null;
  }
  
  const container = document.getElementById(containerId);
  if (container) {

    rideMap = L.map(containerId).setView([18.5204, 73.8567], 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(rideMap);
    
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


function getUserCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          userCurrentLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          console.log("✅ User location obtained:", userCurrentLocation);
          resolve(userCurrentLocation);
        },
        (error) => {
          console.error("❌ Location error:", error);
          reject(error);
        }
      );
    } else {
      reject(new Error("Geolocation not supported"));
    }
  });
}


async function getAddressFromCoords(lat, lng) {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`,
      {
        headers: {
          "User-Agent": "RideShareApp/1.0",
        },
      }
    );
    const data = await response.json();
    return data.display_name || `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  } catch (err) {
    console.error("Error getting address:", err);
    return `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  }
}


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


async function useCurrentLocationAsPickup(inputId, containerId = "map-container") {
  const pickupInput = document.getElementById(inputId);
  if (!pickupInput) return;

  // Show loading state
  pickupInput.value = "Getting your location...";
  pickupInput.disabled = true;

  try {
    const location = await getUserCurrentLocation();
    const address = await getAddressFromCoords(location.lat, location.lng);
    
    pickupInput.value = address;
    pickupInput.disabled = false;

    
    initRideMap(containerId);
    await updatePickupLocation(address, containerId, location);

  } catch (error) {
    console.error("Error getting location:", error);
    pickupInput.value = "";
    pickupInput.disabled = false;
    alert("❌ Could not get your location. Please enable location services.");
  }
}


async function updatePickupLocation(query, containerId = "map-container", predefinedCoords = null) {
  if (!query || query.trim() === "") {
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

 
  const coords = predefinedCoords ? [predefinedCoords.lat, predefinedCoords.lng] : await getCoordinates(query);
  
  if (!coords) {
    console.log("Could not find location for:", query);
    return;
  }

  initRideMap(containerId);

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
    html: '<div style="background: #10b981; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><i class="fas fa-map-marker-alt" style="color: white; font-size: 14px;"></i></div>',
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


async function updateDropoffLocation(query, containerId = "map-container") {
  if (!query || query.trim() === "") {
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
    html: '<div style="background: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><i class="fas fa-flag" style="color: white; font-size: 14px;"></i></div>',
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


async function updateRoute() {
  if (!pickupMarker || !dropMarker || !rideMap) return;

  const pickupCoords = pickupMarker.getLatLng();
  const dropCoords = dropMarker.getLatLng();

  if (routeControl) {
    try {
      rideMap.removeControl(routeControl);
    } catch (e) {
      console.log("Error removing route control:", e);
    }
    routeControl = null;
  }

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

  routeControl.on('routesfound', function(e) {
    const routes = e.routes;
    const route = routes[0];

    const distanceKm = (route.summary.totalDistance / 1000).toFixed(2);
    const durationMin = Math.round(route.summary.totalTime / 60);
    const price = (distanceKm * 15).toFixed(2);

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
  });

  routeControl.on('routingerror', function(e) {
    console.error('❌ Routing error:', e.error);

    const containerId = rideMap._container.id;
    const priceOutputId = containerId === "ride-map-container" ? "ride-price-output" : "price-output";
    const priceOutput = document.getElementById(priceOutputId);
    
    if (priceOutput) {
      priceOutput.innerHTML = `
        <div style="color: #ef4444;">
          ⚠️ Unable to calculate road route. Please try again.
        </div>
      `;
    }
  });
}


async function showPrice() {
  const clickedButton = event && event.target ? event.target : null;
  const isRidePage = clickedButton ? clickedButton.closest('#ride-page') !== null : false;
  
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


function initLiveLocationUpdate() {
 
  const pickupInput = document.getElementById("pickup");
  const dropoffInput = document.getElementById("dropoff");
  

  const ridePickupInput = document.getElementById("ride-pickup");
  const rideDropoffInput = document.getElementById("ride-dropoff");

 
  const locationIcons = document.querySelectorAll('.map-icon');
  locationIcons.forEach(icon => {
    icon.addEventListener('click', function() {
      const isRidePage = this.closest('#ride-page') !== null;
      const inputId = isRidePage ? 'ride-pickup' : 'pickup';
      const containerId = isRidePage ? 'ride-map-container' : 'map-container';
      useCurrentLocationAsPickup(inputId, containerId);
    });
  });

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


if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initLiveLocationUpdate);
} else {
  initLiveLocationUpdate();
}


window.useCurrentLocationAsPickup = useCurrentLocationAsPickup;
window.showPrice = showPrice;


// Add this to your index.js - Enhanced ride booking with request functionality

let currentRideData = null; // Store ride data after price calculation

// Enhanced showPrice function with Request Ride functionality
async function showPrice() {
  const clickedButton = event && event.target ? event.target : null;
  const isRidePage = clickedButton ? clickedButton.closest('#ride-page') !== null : false;
  
  const pickupInputId = isRidePage ? "ride-pickup" : "pickup";
  const dropoffInputId = isRidePage ? "ride-dropoff" : "dropoff";
  const containerId = isRidePage ? "ride-map-container" : "map-container";
  const priceOutputId = isRidePage ? "ride-price-output" : "price-output";
  
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

    // Create route and calculate price
    createRouteWithRequestButton(pickupCoords, dropCoords, pickup, drop, priceOutputId);
  }
}

// Create route and add Request Ride button
function createRouteWithRequestButton(pickupCoords, dropCoords, pickupAddress, dropAddress, priceOutputId) {
  if (!rideMap) return;

  if (routeControl) {
    try {
      rideMap.removeControl(routeControl);
    } catch (e) {
      console.log("Error removing route control:", e);
    }
    routeControl = null;
  }

  routeControl = L.Routing.control({
    waypoints: [
      L.latLng(pickupCoords[0], pickupCoords[1]),
      L.latLng(dropCoords[0], dropCoords[1])
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

  routeControl.on('routesfound', function(e) {
    const routes = e.routes;
    const route = routes[0];

    const distanceKm = (route.summary.totalDistance / 1000).toFixed(2);
    const durationMin = Math.round(route.summary.totalTime / 60);
    const price = (distanceKm * 15).toFixed(2);

    // Store ride data globally
    currentRideData = {
      pickup_lat: pickupCoords[0],
      pickup_lng: pickupCoords[1],
      drop_lat: dropCoords[0],
      drop_lng: dropCoords[1],
      pickup_address: pickupAddress,
      dropoff_address: dropAddress,
      distance: distanceKm,
      fare: price,
      duration: durationMin
    };

    const priceOutput = document.getElementById(priceOutputId);
    
    if (priceOutput) {
      priceOutput.innerHTML = `
        <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 20px; border-radius: 12px; margin-top: 15px;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <strong>📏 Distance:</strong> 
            <span>${distanceKm} km</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <strong>⏱️ Duration:</strong> 
            <span>${durationMin} minutes</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 1.2rem; color: #5fe32e;">
            <strong>💰 Fare:</strong> 
            <span>₹${price}</span>
          </div>
          <button 
            id="request-ride-btn" 
            onclick="requestRide()"
            style="width: 100%; padding: 12px; background: linear-gradient(135deg, #5fe32e, #0ea572); color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 1rem; cursor: pointer; transition: all 0.3s;">
            🚗 Request Ride
          </button>
          <div style="margin-top: 10px; padding: 8px; background: #10b98120; border-left: 3px solid #10b981; font-size: 12px; border-radius: 4px;">
            ✅ <em>Route follows actual roads</em>
          </div>
        </div>
      `;

      // Add hover effect
      const requestBtn = document.getElementById('request-ride-btn');
      if (requestBtn) {
        requestBtn.addEventListener('mouseenter', function() {
          this.style.transform = 'translateY(-2px)';
          this.style.boxShadow = '0 6px 12px rgba(95, 227, 46, 0.3)';
        });
        requestBtn.addEventListener('mouseleave', function() {
          this.style.transform = 'translateY(0)';
          this.style.boxShadow = 'none';
        });
      }
    }
  });

  routeControl.on('routingerror', function(e) {
    console.error('❌ Routing error:', e.error);

    const priceOutput = document.getElementById(priceOutputId);
    
    if (priceOutput) {
      priceOutput.innerHTML = `
        <div style="color: #ef4444; padding: 15px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; margin-top: 15px;">
          ⚠️ Unable to calculate route. Please try again or check your internet connection.
        </div>
      `;
    }
  });
}

// Request ride function
async function requestRide() {
  if (!currentRideData) {
    alert("❌ Please calculate price first!");
    return;
  }

  const requestBtn = document.getElementById('request-ride-btn');
  if (requestBtn) {
    requestBtn.disabled = true;
    requestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Requesting...';
  }

  try {
    console.log("📤 Sending ride request:", currentRideData);

    const response = await fetch('/create_ride', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(currentRideData)
    });

    const data = await response.json();

    if (response.ok) {
      alert(`✅ Ride requested successfully! 
      
Ride ID: ${data.ride_id}
Pickup: ${currentRideData.pickup_address}
Dropoff: ${currentRideData.dropoff_address}
Fare: ₹${currentRideData.fare}

Waiting for driver to accept...`);

      // Clear form
      const pickupInput = document.getElementById('pickup') || document.getElementById('ride-pickup');
      const dropoffInput = document.getElementById('dropoff') || document.getElementById('ride-dropoff');
      if (pickupInput) pickupInput.value = '';
      if (dropoffInput) dropoffInput.value = '';

      const priceOutput = document.getElementById('price-output') || document.getElementById('ride-price-output');
      if (priceOutput) {
        priceOutput.innerHTML = `
          <div style="background: rgba(16, 185, 129, 0.1); padding: 20px; border-radius: 12px; margin-top: 15px; border-left: 4px solid #10b981;">
            <h3 style="color: #10b981; margin-bottom: 10px;">✅ Ride Requested!</h3>
            <p style="margin: 5px 0;">Ride ID: <strong>#${data.ride_id}</strong></p>
            <p style="margin: 5px 0;">Status: <strong>Waiting for driver...</strong></p>
            <p style="margin: 15px 0 10px; font-size: 0.9rem; color: #aaa;">
              Available drivers will see your request on their dashboard.
            </p>
            <button 
              onclick="location.reload()" 
              style="padding: 10px 20px; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; margin-top: 10px;">
              Request Another Ride
            </button>
          </div>
        `;
      }

      currentRideData = null;

    } else {
      alert('❌ ' + (data.error || 'Failed to request ride. Please try again.'));
      
      if (requestBtn) {
        requestBtn.disabled = false;
        requestBtn.innerHTML = '🚗 Request Ride';
      }
    }

  } catch (error) {
    console.error('❌ Request ride error:', error);
    alert('❌ Network error. Please check your connection and try again.');
    
    if (requestBtn) {
      requestBtn.disabled = false;
      requestBtn.innerHTML = '🚗 Request Ride';
    }
  }
}

// Make functions globally available
window.requestRide = requestRide;
window.showPrice = showPrice;





/// new
// Add this to your index.js - User ride tracking functionality
// Add this to your index.js - User ride tracking functionality

let trackingMap;
let userMarker;
let driverMarker;
let trackingRouteControl;
let currentRideId = null;
let trackingInterval = null;

// Initialize tracking map
function initTrackingMap() {
  if (trackingMap) {
    try {
      trackingMap.remove();
    } catch (e) {
      console.log("Error removing tracking map:", e);
    }
    trackingMap = null;
  }
  
  const container = document.getElementById('user-tracking-map');
  if (container) {
    trackingMap = L.map('user-tracking-map').setView([18.5204, 73.8567], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(trackingMap);
    
    setTimeout(() => {
      if (trackingMap) {
        try {
          trackingMap.invalidateSize();
        } catch (e) {
          console.log("Error invalidating map size:", e);
        }
      }
    }, 100);
  }
}

// Show ride status page after requesting ride
function showRideStatusPage(rideId) {
  currentRideId = rideId;
  showPage('ride-status');
  
  // Initialize map
  setTimeout(() => {
    initTrackingMap();
    loadRideStatus();
    
    // Start auto-refresh every 5 seconds
    if (trackingInterval) {
      clearInterval(trackingInterval);
    }
    trackingInterval = setInterval(loadRideStatus, 5000);
  }, 300);
}

// Load and display ride status
async function loadRideStatus() {
  if (!currentRideId) return;

  try {
    const response = await fetch(`/user/ride_status/${currentRideId}`, {
      credentials: 'include'
    });

    if (!response.ok) {
      console.error('Failed to load ride status');
      return;
    }

    const data = await response.json();
    updateRideStatusUI(data);

  } catch (error) {
    console.error('Error loading ride status:', error);
  }
}

// Update UI with ride status
function updateRideStatusUI(data) {
  const { ride, driver } = data;

  // Update status badge
  const statusBadge = document.getElementById('ride-status-badge');
  const statusMessage = document.getElementById('status-message');

  if (ride.status === 'requested') {
    statusBadge.className = 'status-badge waiting';
    statusBadge.innerHTML = '<i class="fas fa-hourglass-half"></i> Waiting for driver...';
    statusMessage.textContent = 'Searching for available drivers nearby...';
  } else if (ride.status === 'accepted') {
    statusBadge.className = 'status-badge accepted';
    statusBadge.innerHTML = '<i class="fas fa-check-circle"></i> Driver Accepted!';
    statusMessage.textContent = 'Your driver is on the way to pick you up!';
    
    // Show driver info
    showDriverInfo(driver);
    // Show payment options
    showPaymentOptions();
  } else if (ride.status === 'in_progress') {
    statusBadge.className = 'status-badge in-progress';
    statusBadge.innerHTML = '<i class="fas fa-car"></i> Ride in Progress';
    statusMessage.textContent = 'Enjoy your ride!';
  } else if (ride.status === 'completed') {
    statusBadge.className = 'status-badge completed';
    statusBadge.innerHTML = '<i class="fas fa-flag-checkered"></i> Ride Completed';
    statusMessage.textContent = 'Thank you for riding with SwiftRide!';
    
    // Stop tracking
    if (trackingInterval) {
      clearInterval(trackingInterval);
      trackingInterval = null;
    }
  }

  // Update trip details
  document.getElementById('pickup-display').textContent = ride.pickup_address || 'N/A';
  document.getElementById('dropoff-display').textContent = ride.dropoff_address || 'N/A';
  document.getElementById('distance-display').textContent = `${ride.distance} km`;
  document.getElementById('fare-display').textContent = `₹${ride.fare}`;

  // Update map
  updateTrackingMap(ride, driver);
}

// Show driver information
function showDriverInfo(driver) {
  if (!driver) return;

  const driverInfoCard = document.getElementById('driver-info-card');
  driverInfoCard.style.display = 'flex';

  document.getElementById('driver-name-display').textContent = driver.full_name || 'Driver';
  document.getElementById('driver-rating-display').textContent = driver.rating || '5.0';
  document.getElementById('driver-vehicle-display').textContent = 
    `${driver.vehicle_type || 'Vehicle'} - ${driver.license_plate || 'N/A'}`;
  document.getElementById('driver-phone-display').innerHTML = 
    `<i class="fas fa-phone"></i> ${driver.phone || 'N/A'}`;
}

// Show payment options with wallet balance
async function showPaymentOptions() {
  const paymentSection = document.getElementById('payment-section');
  const confirmPaymentBtn = document.getElementById('confirm-payment-btn');
  
  if (paymentSection) {
    paymentSection.style.display = 'block';
  }
  
  // Get user's wallet balance
  try {
    const response = await fetch('/user/wallet_balance', {
      credentials: 'include'
    });
    
    if (response.ok) {
      const data = await response.json();
      const walletBalance = data.wallet_balance;
      
      // Update wallet balance display
      document.getElementById('user-wallet-balance').textContent = `₹${walletBalance.toFixed(2)}`;
      
      // Get current ride fare
      const fareText = document.getElementById('fare-display').textContent;
      const fare = parseFloat(fareText.replace('₹', ''));
      
      // Calculate remaining balance
      const remainingBalance = walletBalance - fare;
      
      // Update displays
      document.getElementById('payment-fare-display').textContent = `₹${fare.toFixed(2)}`;
      document.getElementById('remaining-balance').textContent = `₹${remainingBalance.toFixed(2)}`;
      document.getElementById('pay-amount').textContent = fare.toFixed(2);
      
      // Check if user has sufficient balance
      if (remainingBalance >= 0) {
        document.getElementById('remaining-balance').style.color = '#10b981';
        if (confirmPaymentBtn) {
          confirmPaymentBtn.style.display = 'block';
          confirmPaymentBtn.disabled = false;
        }
        // Hide add money button
        const addMoneyBtn = document.getElementById('add-money-btn');
        if (addMoneyBtn) addMoneyBtn.style.display = 'none';
      } else {
        document.getElementById('remaining-balance').style.color = '#ef4444';
        if (confirmPaymentBtn) {
          confirmPaymentBtn.style.display = 'none';
        }
        // Show add money button
        const addMoneyBtn = document.getElementById('add-money-btn');
        if (addMoneyBtn) {
          addMoneyBtn.style.display = 'block';
          addMoneyBtn.onclick = () => {
            const amountNeeded = Math.ceil(fare - walletBalance);
            addMoneyToWallet(amountNeeded);
          };
        }
      }
    }
  } catch (error) {
    console.error('Error fetching wallet balance:', error);
  }
}

// Add money to wallet
async function addMoneyToWallet(suggestedAmount) {
  const amount = prompt(`Enter amount to add to wallet (Minimum: ₹${suggestedAmount}):`, suggestedAmount);
  
  if (!amount || isNaN(amount) || amount <= 0) {
    alert('❌ Invalid amount');
    return;
  }

  try {
    const response = await fetch('/user/add_money', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ amount: parseFloat(amount) })
    });

    const data = await response.json();

    if (response.ok) {
      alert(`✅ ₹${amount} added to your wallet!\nNew Balance: ₹${data.new_balance.toFixed(2)}`);
      // Refresh payment section
      showPaymentOptions();
    } else {
      alert('❌ ' + (data.error || 'Failed to add money'));
    }
  } catch (error) {
    console.error('Error adding money:', error);
    alert('❌ Network error');
  }
}

// Update tracking map with user and driver locations
function updateTrackingMap(ride, driver) {
  if (!trackingMap) return;

  // Remove old markers and route
  if (userMarker) trackingMap.removeLayer(userMarker);
  if (driverMarker) trackingMap.removeLayer(driverMarker);
  if (trackingRouteControl) trackingMap.removeControl(trackingRouteControl);

  // User pickup marker (green)
  const userIcon = L.divIcon({
    className: 'custom-marker',
    html: '<div style="background: #10b981; width: 35px; height: 35px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><i class="fas fa-user" style="color: white; font-size: 16px;"></i></div>',
    iconSize: [35, 35],
    iconAnchor: [17.5, 17.5],
  });

  userMarker = L.marker([ride.pickup_lat, ride.pickup_lng], { icon: userIcon })
    .addTo(trackingMap)
    .bindPopup('<b>📍 Your Location</b><br>Pickup point');

  // If driver accepted, show driver location
  if (ride.status === 'accepted' && driver && driver.current_lat && driver.current_lng) {
    const driverIcon = L.divIcon({
      className: 'custom-marker',
      html: '<div style="background: #3b82f6; width: 40px; height: 40px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><i class="fas fa-car" style="color: white; font-size: 18px;"></i></div>',
      iconSize: [40, 40],
      iconAnchor: [20, 20],
    });

    driverMarker = L.marker([driver.current_lat, driver.current_lng], { icon: driverIcon })
      .addTo(trackingMap)
      .bindPopup(`<b>🚗 ${driver.full_name}</b><br>Driver is coming!`)
      .openPopup();

    // Draw route from driver to pickup
    trackingRouteControl = L.Routing.control({
      waypoints: [
        L.latLng(driver.current_lat, driver.current_lng),
        L.latLng(ride.pickup_lat, ride.pickup_lng)
      ],
      routeWhileDragging: false,
      show: false,
      addWaypoints: false,
      lineOptions: {
        styles: [{ color: '#3b82f6', opacity: 0.8, weight: 5 }]
      },
      createMarker: function() { return null; }
    }).addTo(trackingMap);

    // Fit bounds to show both markers
    const bounds = L.latLngBounds([
      [driver.current_lat, driver.current_lng],
      [ride.pickup_lat, ride.pickup_lng]
    ]);
    trackingMap.fitBounds(bounds, { padding: [50, 50] });

  } else if (ride.status === 'in_progress') {
    // Show dropoff location
    const dropIcon = L.divIcon({
      className: 'custom-marker',
      html: '<div style="background: #ef4444; width: 35px; height: 35px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><i class="fas fa-flag" style="color: white; font-size: 16px;"></i></div>',
      iconSize: [35, 35],
      iconAnchor: [17.5, 17.5],
    });

    const dropMarker = L.marker([ride.drop_lat, ride.drop_lng], { icon: dropIcon })
      .addTo(trackingMap)
      .bindPopup('<b>🎯 Destination</b>');

    // Draw route from pickup to dropoff
    trackingRouteControl = L.Routing.control({
      waypoints: [
        L.latLng(ride.pickup_lat, ride.pickup_lng),
        L.latLng(ride.drop_lat, ride.drop_lng)
      ],
      routeWhileDragging: false,
      show: false,
      addWaypoints: false,
      lineOptions: {
        styles: [{ color: '#10b981', opacity: 0.8, weight: 5 }]
      },
      createMarker: function() { return null; }
    }).addTo(trackingMap);

  } else {
    // Just show pickup location
    trackingMap.setView([ride.pickup_lat, ride.pickup_lng], 15);
  }
}

// Refresh ride status manually
function refreshRideStatus() {
  loadRideStatus();
  alert('✅ Status refreshed!');
}

// Cancel current ride
async function cancelCurrentRide() {
  if (!currentRideId) return;

  if (!confirm('Are you sure you want to cancel this ride?')) {
    return;
  }

  try {
    const response = await fetch(`/user/cancel_ride/${currentRideId}`, {
      method: 'POST',
      credentials: 'include'
    });

    const data = await response.json();

    if (response.ok) {
      alert('✅ Ride cancelled successfully');
      
      // Stop tracking
      if (trackingInterval) {
        clearInterval(trackingInterval);
        trackingInterval = null;
      }
      
      // Go back to home
      showPage('home');
      currentRideId = null;
    } else {
      alert('❌ ' + (data.error || 'Failed to cancel ride'));
    }

  } catch (error) {
    console.error('Error cancelling ride:', error);
    alert('❌ Network error');
  }
}

// Confirm payment
// Replace the confirmPayment function and related code in your index.js

// Confirm payment - FIXED VERSION
async function confirmPayment() {
  if (!currentRideId) return;

  const confirmBtn = document.getElementById('confirm-payment-btn');
  if (confirmBtn) {
    confirmBtn.disabled = true;
    confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing Payment...';
  }

  try {
    const response = await fetch('/user/confirm_payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        ride_id: currentRideId
        // No payment_method needed - always wallet
      })
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✅ Payment successful:', data);
      
      // Payment successful
      const paymentSection = document.getElementById('payment-section');
      if (paymentSection) {
        paymentSection.innerHTML = `
          <div style="text-align: center; padding: 30px; background: rgba(16, 185, 129, 0.1); border-radius: 12px; border: 2px solid #10b981;">
            <i class="fas fa-check-circle" style="font-size: 4rem; color: #10b981; margin-bottom: 20px;"></i>
            <h3 style="margin: 0 0 15px; color: #10b981;">Payment Successful!</h3>
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 8px; margin: 20px 0;">
              <div style="display: flex; justify-content: space-between; margin: 10px 0; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                <span>Amount Paid:</span>
                <strong style="color: #10b981;">₹${data.fare.toFixed(2)}</strong>
              </div>
              <div style="display: flex; justify-content: space-between; margin: 10px 0; padding: 8px 0;">
                <span>Your New Balance:</span>
                <strong style="color: #10b981;">₹${data.user_new_balance.toFixed(2)}</strong>
              </div>
            </div>
            <p style="margin: 15px 0 0; color: #aaa; font-size: 0.9rem;">
              <i class="fas fa-info-circle"></i> Money has been transferred from your wallet to driver's wallet
            </p>
          </div>
        `;
      }

      // Update navbar wallet balance
      if (typeof updateNavbarWalletBalance === 'function') {
        updateNavbarWalletBalance();
      }

      alert(`✅ Payment Successful!\n\nAmount: ₹${data.fare}\nYour new wallet balance: ₹${data.user_new_balance.toFixed(2)}`);

    } else {
      if (confirmBtn) {
        confirmBtn.disabled = false;
        confirmBtn.innerHTML = '<i class="fas fa-check-circle"></i> Pay ₹<span id="pay-amount">0</span> from Wallet';
      }
      
      if (data.error === 'Insufficient wallet balance') {
        alert(`❌ Insufficient Balance!\n\nRequired: ₹${data.required}\nAvailable: ₹${data.available}\n\nPlease add money to your wallet.`);
        // Show add money button
        const addMoneyBtn = document.getElementById('add-money-btn');
        if (addMoneyBtn) {
          addMoneyBtn.style.display = 'block';
        }
      } else {
        alert('❌ ' + (data.error || 'Payment failed'));
      }
    }

  } catch (error) {
    console.error('Error confirming payment:', error);
    alert('❌ Network error during payment');
    
    if (confirmBtn) {
      confirmBtn.disabled = false;
      confirmBtn.innerHTML = '<i class="fas fa-check-circle"></i> Pay ₹<span id="pay-amount">0</span> from Wallet';
    }
  }
}

// Show payment options with wallet balance - FIXED VERSION
async function showPaymentOptions() {
  const paymentSection = document.getElementById('payment-section');
  const confirmPaymentBtn = document.getElementById('confirm-payment-btn');
  
  if (paymentSection) {
    paymentSection.style.display = 'block';
  }
  
  // Get user's wallet balance
  try {
    const response = await fetch('/user/wallet_balance', {
      credentials: 'include'
    });
    
    if (response.ok) {
      const data = await response.json();
      const walletBalance = data.wallet_balance;
      
      console.log('💰 Wallet balance:', walletBalance);
      
      // Update wallet balance display
      const walletBalanceEl = document.getElementById('user-wallet-balance');
      if (walletBalanceEl) {
        walletBalanceEl.textContent = `₹${walletBalance.toFixed(2)}`;
      }
      
      // Get current ride fare
      const fareText = document.getElementById('fare-display').textContent;
      const fare = parseFloat(fareText.replace('₹', ''));
      
      console.log('💵 Fare:', fare);
      
      // Calculate remaining balance
      const remainingBalance = walletBalance - fare;
      
      // Update displays
      const fareDisplayEl = document.getElementById('payment-fare-display');
      if (fareDisplayEl) {
        fareDisplayEl.textContent = `₹${fare.toFixed(2)}`;
      }
      
      const remainingEl = document.getElementById('remaining-balance');
      if (remainingEl) {
        remainingEl.textContent = `₹${remainingBalance.toFixed(2)}`;
      }
      
      const payAmountEl = document.getElementById('pay-amount');
      if (payAmountEl) {
        payAmountEl.textContent = fare.toFixed(2);
      }
      
      // Check if user has sufficient balance
      if (remainingBalance >= 0) {
        if (remainingEl) {
          remainingEl.style.color = '#10b981';
        }
        if (confirmPaymentBtn) {
          confirmPaymentBtn.style.display = 'block';
          confirmPaymentBtn.disabled = false;
        }
        // Hide add money button
        const addMoneyBtn = document.getElementById('add-money-btn');
        if (addMoneyBtn) addMoneyBtn.style.display = 'none';
        
        console.log('✅ Sufficient balance - showing pay button');
      } else {
        if (remainingEl) {
          remainingEl.style.color = '#ef4444';
        }
        if (confirmPaymentBtn) {
          confirmPaymentBtn.style.display = 'none';
        }
        // Show add money button
        const addMoneyBtn = document.getElementById('add-money-btn');
        if (addMoneyBtn) {
          addMoneyBtn.style.display = 'block';
          addMoneyBtn.onclick = () => {
            const amountNeeded = Math.ceil(fare - walletBalance);
            addMoneyToWallet(amountNeeded);
          };
        }
        
        console.log('❌ Insufficient balance - showing add money button');
      }
    } else {
      console.error('Failed to fetch wallet balance:', response.status);
    }
  } catch (error) {
    console.error('Error fetching wallet balance:', error);
  }
}

// Update the loadRideStatus function to show payment section correctly
async function loadRideStatus() {
  if (!currentRideId) return;

  try {
    const response = await fetch(`/user/ride_status/${currentRideId}`, {
      credentials: 'include'
    });

    if (!response.ok) {
      console.error('Failed to load ride status');
      return;
    }

    const data = await response.json();
    console.log('📊 Ride status:', data);
    updateRideStatusUI(data);

  } catch (error) {
    console.error('Error loading ride status:', error);
  }
}

// Update UI with ride status - FIXED VERSION
function updateRideStatusUI(data) {
  const { ride, driver } = data;

  console.log('🔄 Updating UI - Ride status:', ride.status);

  // Update status badge
  const statusBadge = document.getElementById('ride-status-badge');
  const statusMessage = document.getElementById('status-message');

  if (ride.status === 'requested') {
    statusBadge.className = 'status-badge waiting';
    statusBadge.innerHTML = '<i class="fas fa-hourglass-half"></i> Waiting for driver...';
    statusMessage.textContent = 'Searching for available drivers nearby...';
    console.log('⏳ Status: Waiting for driver');
  } else if (ride.status === 'accepted') {
    statusBadge.className = 'status-badge accepted';
    statusBadge.innerHTML = '<i class="fas fa-check-circle"></i> Driver Accepted!';
    statusMessage.textContent = 'Your driver is on the way to pick you up!';
    
    console.log('✅ Status: Accepted by driver');
    
    // Show driver info
    showDriverInfo(driver);
    // Show payment options
    showPaymentOptions();
  } else if (ride.status === 'in_progress') {
    statusBadge.className = 'status-badge in-progress';
    statusBadge.innerHTML = '<i class="fas fa-car"></i> Ride in Progress';
    statusMessage.textContent = 'Enjoy your ride!';
    console.log('🚗 Status: In progress');
  } else if (ride.status === 'completed') {
    statusBadge.className = 'status-badge completed';
    statusBadge.innerHTML = '<i class="fas fa-flag-checkered"></i> Ride Completed';
    statusMessage.textContent = 'Thank you for riding with SwiftRide!';
    
    console.log('🏁 Status: Completed');
    
    // Stop tracking
    if (trackingInterval) {
      clearInterval(trackingInterval);
      trackingInterval = null;
    }
  }

  // Update trip details
  document.getElementById('pickup-display').textContent = ride.pickup_address || 'N/A';
  document.getElementById('dropoff-display').textContent = ride.dropoff_address || 'N/A';
  document.getElementById('distance-display').textContent = `${ride.distance} km`;
  document.getElementById('fare-display').textContent = `₹${ride.fare}`;

  // Update map
  updateTrackingMap(ride, driver);
}

// Make sure confirmPayment is called when button is clicked
document.addEventListener('DOMContentLoaded', function() {
  console.log('🎬 Setting up payment button listener');
  
  // Use event delegation since the button is dynamically created
  document.body.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'confirm-payment-btn') {
      console.log('💳 Payment button clicked');
      confirmPayment();
    }
  });
});

// Update the requestRide function to show status page
async function requestRide() {
  if (!currentRideData) {
    alert("❌ Please calculate price first!");
    return;
  }

  const requestBtn = document.getElementById('request-ride-btn');
  if (requestBtn) {
    requestBtn.disabled = true;
    requestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Requesting...';
  }

  try {
    console.log("📤 Sending ride request:", currentRideData);

    const response = await fetch('/create_ride', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(currentRideData)
    });

    const data = await response.json();

    if (response.ok) {
      // Show ride status page instead of alert
      showRideStatusPage(data.ride_id);
      currentRideData = null;
    } else {
      alert('❌ ' + (data.error || 'Failed to request ride. Please try again.'));
      
      if (requestBtn) {
        requestBtn.disabled = false;
        requestBtn.innerHTML = '🚗 Request Ride';
      }
    }

  } catch (error) {
    console.error('❌ Request ride error:', error);
    alert('❌ Network error. Please check your connection and try again.');
    
    if (requestBtn) {
      requestBtn.disabled = false;
      requestBtn.innerHTML = '🚗 Request Ride';
    }
  }
}

// Add event listener for payment confirmation
document.addEventListener('DOMContentLoaded', function() {
  const confirmPaymentBtn = document.getElementById('confirm-payment-btn');
  if (confirmPaymentBtn) {
    confirmPaymentBtn.addEventListener('click', confirmPayment);
  }
});

// Cleanup when leaving ride status page
window.addEventListener('beforeunload', function() {
  if (trackingInterval) {
    clearInterval(trackingInterval);
  }
});







// Add these enhanced features to your index.js

// ==================== REAL-TIME RIDE STATUS UPDATES ====================

let statusUpdateInterval = null;

// Start polling for ride status updates
function startRideStatusPolling(rideId) {
  // Clear any existing interval
  if (statusUpdateInterval) {
    clearInterval(statusUpdateInterval);
  }
  
  // Initial update
  updateRideStatus(rideId);
  
  // Poll every 3 seconds
  statusUpdateInterval = setInterval(() => {
    updateRideStatus(rideId);
  }, 3000);
}

// Stop polling
function stopRideStatusPolling() {
  if (statusUpdateInterval) {
    clearInterval(statusUpdateInterval);
    statusUpdateInterval = null;
  }
}

// Update ride status from server
async function updateRideStatus(rideId) {
  try {
    const response = await fetch(`/user/ride_updates/${rideId}`, {
      credentials: 'include'
    });
    
    if (!response.ok) {
      console.error('Failed to fetch ride updates');
      return;
    }
    
    const data = await response.json();
    handleRideStatusUpdate(data.ride);
    
  } catch (error) {
    console.error('Error fetching ride updates:', error);
  }
}

// Handle ride status updates
function handleRideStatusUpdate(ride) {
  const statusBadge = document.getElementById('ride-status-badge');
  const statusMessage = document.getElementById('status-message');
  
  if (!statusBadge || !statusMessage) return;
  
  switch(ride.status) {
    case 'requested':
      statusBadge.className = 'status-badge waiting';
      statusBadge.innerHTML = '<i class="fas fa-hourglass-half"></i> Waiting for driver...';
      statusMessage.textContent = 'Searching for available drivers nearby...';
      break;
      
    case 'accepted':
      statusBadge.className = 'status-badge accepted';
      statusBadge.innerHTML = '<i class="fas fa-check-circle"></i> Driver Accepted!';
      statusMessage.textContent = `${ride.driver_name} is on the way to pick you up!`;
      
      // Show driver info
      showDriverInfoCard(ride);
      
      // Update map with driver location
      if (ride.driver_lat && ride.driver_lng) {
        updateDriverLocationOnMap(ride.driver_lat, ride.driver_lng);
      }
      break;
      
    case 'in_progress':
      statusBadge.className = 'status-badge in-progress';
      statusBadge.innerHTML = '<i class="fas fa-car"></i> Ride in Progress';
      statusMessage.textContent = 'Enjoy your ride! Your driver is taking you to your destination.';
      break;
      
    case 'completed':
      statusBadge.className = 'status-badge completed';
      statusBadge.innerHTML = '<i class="fas fa-flag-checkered"></i> Ride Completed';
      statusMessage.textContent = 'Your ride is complete! Please proceed with payment.';
      
      // Stop polling
      stopRideStatusPolling();
      
      // Show payment options if not paid
      if (ride.payment_status !== 'paid') {
        showPaymentSection(ride);
      }
      break;
      
    case 'cancelled':
      statusBadge.className = 'status-badge cancelled';
      statusBadge.innerHTML = '<i class="fas fa-times-circle"></i> Ride Cancelled';
      statusMessage.textContent = 'This ride has been cancelled.';
      stopRideStatusPolling();
      break;
  }
}

// Show driver info card
function showDriverInfoCard(ride) {
  const driverCard = document.getElementById('driver-info-card');
  if (!driverCard) return;
  
  driverCard.style.display = 'flex';
  
  document.getElementById('driver-name-display').textContent = ride.driver_name || 'Driver';
  document.getElementById('driver-rating-display').textContent = ride.driver_rating || '5.0';
  document.getElementById('driver-vehicle-display').textContent = 
    `${ride.vehicle_type || 'Vehicle'} - ${ride.license_plate || 'N/A'}`;
  document.getElementById('driver-phone-display').innerHTML = 
    `<i class="fas fa-phone"></i> ${ride.driver_phone || 'N/A'}`;
}

// Show payment section
function showPaymentSection(ride) {
  const paymentSection = document.getElementById('payment-section');
  if (paymentSection) {
    paymentSection.style.display = 'block';
    loadUserWalletBalance(ride.fare);
  }
}

// Load user wallet balance and check if sufficient
async function loadUserWalletBalance(fareAmount) {
  try {
    const response = await fetch('/user/wallet_balance', {
      credentials: 'include'
    });
    
    if (!response.ok) {
      console.error('Failed to fetch wallet balance');
      return;
    }
    
    const data = await response.json();
    const walletBalance = data.wallet_balance;
    
    // Update displays
    document.getElementById('user-wallet-balance').textContent = `₹${walletBalance.toFixed(2)}`;
    document.getElementById('payment-fare-display').textContent = `₹${fareAmount}`;
    
    const remainingBalance = walletBalance - fareAmount;
    document.getElementById('remaining-balance').textContent = `₹${remainingBalance.toFixed(2)}`;
    document.getElementById('pay-amount').textContent = fareAmount.toFixed(2);
    
    const remainingEl = document.getElementById('remaining-balance');
    const confirmBtn = document.getElementById('confirm-payment-btn');
    const addMoneyBtn = document.getElementById('add-money-btn');
    
    if (remainingBalance >= 0) {
      // Sufficient balance
      remainingEl.style.color = '#10b981';
      if (confirmBtn) {
        confirmBtn.style.display = 'block';
        confirmBtn.disabled = false;
      }
      if (addMoneyBtn) {
        addMoneyBtn.style.display = 'none';
      }
    } else {
      // Insufficient balance
      remainingEl.style.color = '#ef4444';
      if (confirmBtn) {
        confirmBtn.style.display = 'none';
      }
      if (addMoneyBtn) {
        addMoneyBtn.style.display = 'block';
        addMoneyBtn.onclick = () => {
          const needed = Math.ceil(fareAmount - walletBalance);
          promptAddMoney(needed);
        };
      }
    }
    
  } catch (error) {
    console.error('Error loading wallet balance:', error);
  }
}

// Prompt user to add money to wallet
function promptAddMoney(minimumAmount) {
  const amount = prompt(
    `Your wallet needs ₹${minimumAmount} more.\n\nEnter amount to add (minimum ₹${minimumAmount}):`,
    minimumAmount
  );
  
  if (!amount || isNaN(amount) || parseFloat(amount) < minimumAmount) {
    alert('❌ Invalid amount. Please add at least ₹' + minimumAmount);
    return;
  }
  
  addMoneyToUserWallet(parseFloat(amount));
}

// Add money to user wallet
async function addMoneyToUserWallet(amount) {
  try {
    const response = await fetch('/user/add_money', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ amount: amount })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert(`✅ ₹${amount} added successfully!\n\nNew wallet balance: ₹${data.new_balance.toFixed(2)}`);
      
      // Refresh payment section
      const fareText = document.getElementById('fare-display').textContent;
      const fare = parseFloat(fareText.replace('₹', ''));
      loadUserWalletBalance(fare);
      
      // Update navbar wallet
      if (typeof updateNavbarWalletBalance === 'function') {
        updateNavbarWalletBalance();
      }
    } else {
      alert('❌ ' + (data.error || 'Failed to add money'));
    }
  } catch (error) {
    console.error('Error adding money:', error);
    alert('❌ Network error');
  }
}

// ==================== ENHANCED RIDE REQUEST ====================

// Enhanced request ride with better UX
async function requestRideEnhanced() {
  if (!currentRideData) {
    alert("❌ Please calculate the price first!");
    return;
  }
  
  // Show confirmation dialog with ride details
  const confirmMsg = `
🚗 Confirm Ride Request

📍 Pickup: ${currentRideData.pickup_address}
🎯 Drop: ${currentRideData.dropoff_address}
📏 Distance: ${currentRideData.distance} km
⏱️ Duration: ~${currentRideData.duration} min
💰 Fare: ₹${currentRideData.fare}

Press OK to request this ride.
  `.trim();
  
  if (!confirm(confirmMsg)) {
    return;
  }
  
  const requestBtn = document.getElementById('request-ride-btn');
  if (requestBtn) {
    requestBtn.disabled = true;
    requestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Requesting...';
  }
  
  try {
    const response = await fetch('/create_ride', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(currentRideData)
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('✅ Ride requested successfully:', data.ride_id);
      
      // Clear current ride data
      currentRideData = null;
      
      // Show ride status page and start polling
      showRideStatusPage(data.ride_id);
      startRideStatusPolling(data.ride_id);
      
    } else {
      alert('❌ ' + (data.error || 'Failed to request ride'));
      
      if (requestBtn) {
        requestBtn.disabled = false;
        requestBtn.innerHTML = '🚗 Request Ride';
      }
    }
    
  } catch (error) {
    console.error('❌ Request ride error:', error);
    alert('❌ Network error. Please check your connection.');
    
    if (requestBtn) {
      requestBtn.disabled = false;
      requestBtn.innerHTML = '🚗 Request Ride';
    }
  }
}

// Override the original requestRide function
window.requestRide = requestRideEnhanced;

// ==================== DRIVER DASHBOARD ENHANCEMENTS ====================

// Auto-refresh driver dashboard
function initDriverDashboardPolling() {
  // Refresh available rides every 10 seconds
  setInterval(loadAvailableRidesForDriver, 10000);
  
  // Update driver location every 30 seconds
  setInterval(updateDriverCurrentLocation, 30000);
}

// Load available rides for driver
async function loadAvailableRidesForDriver() {
  try {
    const response = await fetch('/driver/available_rides', {
      credentials: 'include'
    });
    
    if (!response.ok) return;
    
    const data = await response.json();
    updateDriverRidesList(data.rides);
    
  } catch (error) {
    console.error('Error loading rides:', error);
  }
}

// Update rides list in driver dashboard
function updateDriverRidesList(rides) {
  const container = document.getElementById('available-rides');
  if (!container) return;
  
  if (!rides || rides.length === 0) {
    container.innerHTML = `
      <div class="ride-card">
        <p style="text-align: center; color: #aaa; padding: 20px;">
          <i class="fas fa-hourglass-half" style="font-size: 2rem; display: block; margin-bottom: 10px;"></i>
          No ride requests at the moment<br>
          <small>New rides will appear automatically</small>
        </p>
      </div>
    `;
    return;
  }
  
  container.innerHTML = rides.map(ride => `
    <div class="ride-card" data-ride-id="${ride.ride_id}">
      <div class="ride-header">
        <div class="ride-id">Ride #${ride.ride_id}</div>
        <div class="ride-status">New Request</div>
      </div>
      <div class="ride-details">
        <div class="ride-detail">
          <span><i class="fas fa-user"></i> Passenger</span>
          <span>${ride.user_firstName} ${ride.user_lastName}</span>
        </div>
        <div class="ride-detail">
          <span><i class="fas fa-map-marker-alt"></i> Pickup</span>
          <span>${ride.pickup_address || 'N/A'}</span>
        </div>
        <div class="ride-detail">
          <span><i class="fas fa-flag"></i> Dropoff</span>
          <span>${ride.dropoff_address || 'N/A'}</span>
        </div>
        <div class="ride-detail">
          <span><i class="fas fa-road"></i> Distance</span>
          <span>${ride.distance} km</span>
        </div>
        <div class="ride-detail" style="color: #10b981; font-weight: bold;">
          <span><i class="fas fa-rupee-sign"></i> Fare</span>
          <span>₹${ride.fare}</span>
        </div>
        <div class="ride-detail">
          <span><i class="fas fa-clock"></i> Requested</span>
          <span>${new Date(ride.requested_at).toLocaleTimeString()}</span>
        </div>
      </div>
      <div class="ride-actions">
        <button class="btn btn-danger" onclick="rejectRide(${ride.ride_id})">
          <i class="fas fa-times"></i> Reject
        </button>
        <button class="btn btn-outline" onclick="viewRideOnMap(${ride.pickup_lat}, ${ride.pickup_lng}, ${ride.drop_lat}, ${ride.drop_lng})">
          <i class="fas fa-map"></i> View Map
        </button>
        <button class="btn btn-primary" onclick="acceptRide(${ride.ride_id})">
          <i class="fas fa-check"></i> Accept
        </button>
      </div>
    </div>
  `).join('');
}

// Reject ride
async function rejectRide(rideId) {
  if (!confirm('Are you sure you want to reject this ride?')) {
    return;
  }
  
  try {
    const response = await fetch(`/driver/reject_ride/${rideId}`, {
      method: 'POST',
      credentials: 'include'
    });
    
    if (response.ok) {
      alert('✅ Ride rejected');
      loadAvailableRidesForDriver();
    } else {
      alert('❌ Failed to reject ride');
    }
  } catch (error) {
    console.error('Error rejecting ride:', error);
    alert('❌ Network error');
  }
}

// Update driver's current location
async function updateDriverCurrentLocation() {
  if (!navigator.geolocation) return;
  
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      try {
        await fetch('/driver/update_location', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          })
        });
        console.log('📍 Location updated');
      } catch (error) {
        console.error('Failed to update location:', error);
      }
    },
    (error) => {
      console.error('Geolocation error:', error);
    },
    { enableHighAccuracy: true }
  );
}

// Initialize driver dashboard when on that page
if (window.location.pathname === '/driver/dashboard') {
  document.addEventListener('DOMContentLoaded', initDriverDashboardPolling);
}

// Make functions globally available
window.rejectRide = rejectRide;
window.startRideStatusPolling = startRideStatusPolling;
window.stopRideStatusPolling = stopRideStatusPolling;

    // Call this whenever the ride page becomes visible
    function showRidePage() {
      document.getElementById('ride-page').style.display = 'block';
      
      // Initialize map for ride page
      initRideMap("ride-map-container");
    }

   