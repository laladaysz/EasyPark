import React from 'react';
import styles from './Modal.module.css';


interface ModalProps {
  isOpen: boolean;
}

export function Modal({ isOpen }: ModalProps) {
  if (isOpen) {
    return (
      <>
      <div className={styles.background}>
        <div className={styles.modal_container}>
            <div className={styles.modal_content}>
                <div className={styles.info_ocupante}>
                    <div className={styles.title}>
                        <p>VAGA PIPIPI</p>
                    </div>
                </div>
            </div>
        </div>
      </div>
      </>
    );
  }

  return null;
}
