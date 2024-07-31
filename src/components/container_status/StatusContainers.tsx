import styles from './StatusContainer.module.css'

export function StatusContainers(){
    return(
        <div className={styles.container}>   
            <div className={styles.container_title}>
                <span className={styles.title}><b>Disponibilidade</b> de vagas</span>
            </div>

            <div className={styles.containers_status}>
                <div className={styles.column}>
                    <p className={styles.title_column}><b>Disposição</b> das vagas</p>
                    <p>vagas ocupadas: <span className={styles.red}>vermelho</span></p>
                    <p>vagas desocupadas: <span className={styles.green}>verde</span></p>
                </div>
                <div className={styles.column}>
                    <p className={styles.title_column}>Vagas a serem <b>monitoradas</b>:</p>
                    <div className={styles.container_col}>
                        <div className={styles.col}><p className={styles.p_a}>A1</p></div>
                        <div className={styles.col}><p className={styles.p_a}>A2</p></div>
                        <div className={styles.col}><p className={styles.p_a}>A3</p></div>
                        <div className={styles.col}><p className={styles.p_a}>A4</p></div>
                        <div className={styles.col}><p className={styles.p_a}>A5</p></div>
                        <div className={styles.col}><p className={styles.p_a}>A6</p></div>
                        <div className={styles.col}><p className={styles.p_a}>A7</p></div>
                        <div className={styles.col}><p className={styles.p_a}>A8</p></div>
                    </div>
                </div>
            </div>
        </div>
    )
}