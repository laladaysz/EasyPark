import styles from './Monitoramento.module.css';
import { Modal } from '../modal/Modal';
import { useState } from 'react';

export function Monitoramento() {
  const [openModal, setOpenModal] = useState(false);

  return (
    <>
      <div className={styles.container}>
        <div className={styles.content}>
          <div className={styles.title}>
            <p><b>Selecione</b> a vaga que deseja</p><p><b>visualizar</b></p>
          </div>
          <div className={styles.vagas_container}>
            <hr />
          </div>
          <div className={styles.grid_linhas}>
            <div className={styles.linha_vertical_transparente}>
              <button onClick={() => setOpenModal(true)} className={styles.vaga}></button>
              <p className={styles.vaga_marcacao}>A1</p>
            </div>
            <div className={styles.linha_vertical}>
              <button onClick={() => setOpenModal(true)} className={styles.vaga}></button>
              <p className={styles.vaga_marcacao}>A2</p>
            </div>
            <div className={styles.linha_vertical}>
              <button onClick={() => setOpenModal(true)} className={styles.vaga}></button>
              <p className={styles.vaga_marcacao}>A3</p>
            </div>
            <div className={styles.linha_vertical}>
              <button onClick={() => setOpenModal(true)} className={styles.vaga}></button>
              <p className={styles.vaga_marcacao}>A4</p>
            </div>
            <div className={styles.linha_vertical}>
              <button onClick={() => setOpenModal(true)} className={styles.vaga}></button>
              <p className={styles.vaga_marcacao}>A5</p>
            </div>
            <div className={styles.linha_vertical}>
              <button onClick={() => setOpenModal(true)} className={styles.vaga}></button>
              <p className={styles.vaga_marcacao}>A6</p>
            </div>
          </div>
          <Modal isOpen={openModal} onClose={() => setOpenModal(false)} />
        </div>
      </div>
    </>
  );
}
