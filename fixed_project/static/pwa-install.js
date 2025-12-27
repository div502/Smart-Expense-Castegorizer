// PWA Installation Script
let deferredPrompt;
let installButton;
let installButtonHeader;

window.addEventListener('beforeinstallprompt', (e) => {
  console.log('beforeinstallprompt fired');
  // Prevent Chrome 67 and earlier from automatically showing the prompt
  e.preventDefault();
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  
  // Show install buttons
  installButton = document.getElementById('install-button');
  installButtonHeader = document.getElementById('install-button-header');
  
  if (installButton) {
    installButton.style.display = 'block';
    installButton.addEventListener('click', installApp);
  }
  
  if (installButtonHeader) {
    installButtonHeader.style.display = 'block';
    installButtonHeader.addEventListener('click', installApp);
  }
});

function installApp() {
  console.log('Install button clicked');
  if (deferredPrompt) {
    // Show the prompt
    deferredPrompt.prompt();
    
    // Wait for the user to respond to the prompt
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the install prompt');
        // Hide the install buttons
        if (installButton) {
          installButton.style.display = 'none';
        }
        if (installButtonHeader) {
          installButtonHeader.style.display = 'none';
        }
      } else {
        console.log('User dismissed the install prompt');
      }
      deferredPrompt = null;
    });
  }
}

// Check if app is already installed
window.addEventListener('appinstalled', (evt) => {
  console.log('App was installed');
  if (installButton) {
    installButton.style.display = 'none';
  }
  if (installButtonHeader) {
    installButtonHeader.style.display = 'none';
  }
});

// Register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered: ', registration);
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Check if app is running in standalone mode
function isStandalone() {
  return window.matchMedia('(display-mode: standalone)').matches || 
         window.navigator.standalone === true;
}

// Show different UI based on installation status
document.addEventListener('DOMContentLoaded', () => {
  if (isStandalone()) {
    console.log('App is running in standalone mode');
    // Hide install buttons if app is already installed
    const installBtn = document.getElementById('install-button');
    const installBtnHeader = document.getElementById('install-button-header');
    
    if (installBtn) {
      installBtn.style.display = 'none';
    }
    if (installBtnHeader) {
      installBtnHeader.style.display = 'none';
    }
  }
});