//import React from 'react';
import styles from './Modal.module.css';


interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: StatusData
}

export function Modal({ isOpen, onClose }: ModalProps) {
  if (isOpen) {
    return (
      <>
      <div className={styles.background} onClick={onClose}>
        <div className={styles.modal_container} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modal_content}>
              <div className={styles.info_occupant}>
                  <div className={styles.title}>
                    <p>VAGA PIPIPI</p>
                  </div>
                  <div className={styles.status_content}>
                    <p>Status da vaga: <span className={styles.modal_status_vaga}>OCUPADA</span></p>
                  </div>
                  <div className={styles.name_occupant_content}>
                    <p>Nome do ocupante: <span className={styles.name}>pipipi popopo</span></p>
                  </div>
                  <div className={styles.place_number_content}>
                    <p>Placa do carro: <span className={styles.place_number}>HDR9X36</span></p>
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
