import React, { useState } from 'react';
import LoginModal from './LoginModal';
import RegisterModal from './RegisterModal';

interface AuthManagerProps {
  children: React.ReactNode;
}

export default function AuthManager({ children }: AuthManagerProps) {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  const openLogin = () => {
    setShowRegister(false);
    setShowLogin(true);
  };

  const openRegister = () => {
    setShowLogin(false);
    setShowRegister(true);
  };

  const closeModals = () => {
    setShowLogin(false);
    setShowRegister(false);
  };

  return (
    <>
      {/* Render children with auth functions */}
      {typeof children === 'object' && children !== null && 'type' in children
        ? React.cloneElement(children as React.ReactElement, {
            onOpenLogin: openLogin,
            onOpenRegister: openRegister,
          })
        : children}

      {/* Pass auth functions to any components that need them */}
      <div style={{ display: 'none' }} data-auth-functions={{ openLogin, openRegister }} />

      {/* Modals */}
      <LoginModal
        isOpen={showLogin}
        onClose={closeModals}
        onSwitchToRegister={openRegister}
      />
      <RegisterModal
        isOpen={showRegister}
        onClose={closeModals}
        onSwitchToLogin={openLogin}
      />
    </>
  );
}