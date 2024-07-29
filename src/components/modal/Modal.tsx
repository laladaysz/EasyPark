//import React from 'react';
import styles from './Modal.module.css';
import { StatusData, OwnerData } from '../monitoramento/Monitoramento';



interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: StatusData | null;
  ownerData: OwnerData | null;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, data, ownerData }) => {
  if (!isOpen) return null;
  if (isOpen) {
    return (
      <>
      <div className={styles.background} onClick={onClose}>
        <div className={styles.modal_container} onClick={(e) => e.stopPropagation()}>
            <div className={styles.modal_content}>
              <div className={styles.info_occupant}>
              <div className={styles.title}>
                      <p>VAGA {data?.spot_id ?? 'Carregando...'}</p>
                  </div>
                  <div className={styles.status_content}>
                      <p>Status da vaga: <span className={styles.modal_status_vaga}>{data?.status.toUpperCase() ?? 'Carregando...'}</span></p>
                  </div>
                  <div className={styles.name_occupant_content}>
                      <p>Área do ocupante: <span className={styles.name}>{ownerData?.area ?? 'Carregando...'}</span></p>
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
