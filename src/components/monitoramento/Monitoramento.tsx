import styles from './Monitoramento.module.css'
import { Modal } from '../modal/Modal'
import { useEffect, useState } from 'react'
import axios from 'axios';

  export interface StatusData {
    spot_id: string;
    status: string;
  }

  export interface PlateData{
    spot_id: string;
    plate_number: string;
  }

  export interface OwnerData {
    area: string;
    plate_number: string;
  }

export function Monitoramento(){
    const [statusData, setStatusData] = useState<Record<string, StatusData[]>>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    const [openModal, setOpenModal] = useState(false);
    const [selectedSpot, setSelectedSpot] = useState<StatusData | null>(null);
    const [ownerData, setOwnerData] = useState<OwnerData | null>(null);



    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await axios.get<StatusData[]>('http://127.0.0.1:8000/api/status');
            const data = response.data;
    
            // Organizar os dados por vaga (spot_id)
            const organizedData = data.reduce<Record<string, StatusData[]>>((acc, item) => {
              if (!acc[item.spot_id]) {
                acc[item.spot_id] = [];
              }
              acc[item.spot_id].push(item);
              return acc;
            }, {});
    
            setStatusData(organizedData);
            setLoading(false);
          } catch (error) {
            setError(error as Error);
            setLoading(false);
            console.log(`Erro: ${error}`)
          }
        };
    
        fetchData();
        const intervalId = setInterval(fetchData, 5000);

        // Cleanup do intervalo
        return () => clearInterval(intervalId);
      }, []);

      const fetchPlateData = async (spotId: string): Promise<PlateData | null> => {
        try {
            const response = await axios.get<PlateData[]>('http://127.0.0.1:8000/api/plate/');
            const plates = response.data;
            
            const plate = plates.find(p => p.spot_id === spotId);
    
            if (plate) {
                return plate;
            } else {
                console.log(`Placa não encontrada para spotId ${spotId}`);
                return null;
            }
        } catch (error) {
            console.log(`Erro ao buscar dados da placa: ${error}`);
            return null;
        }
    };

    const fetchOwnerData = async (plateNumber: string): Promise<OwnerData | null> => {
      try {
        const response = await axios.get<OwnerData[]>('http://127.0.0.1:8000/api/owners/');
        const owners = response.data

        const owner = owners.find(o => o.plate_number === plateNumber);

        if (owner) {
          return owner;
      } else {
          console.log(`Proprietário não encontrado para placa ${plateNumber}`);
          return null;
      }

      } catch (error) {
        console.log(`Erro ao buscar dados do proprietário: ${error}`);
        return null;
      }
    };

      if (loading) {
        return <div>Carregando...</div>;
      }
    
      if (error) {
        return <div>Erro: {error.message}</div>;
      }

      const handleOpenModal = async (spot: StatusData) => {
        if (spot.status === 'Occupied') {
          setSelectedSpot(spot);
        try {
            const plateData = await fetchPlateData(spot.spot_id);
            if (plateData) {               
                const ownerData = await fetchOwnerData(plateData.plate_number);
                if (ownerData) {
                    setOwnerData(ownerData);
                    setOpenModal(true);
                }
            }
        } catch (error) {
            console.log(`Erro ao abrir o modal: ${error}`);
        }
      }
    };
    

  return(
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
                    {Object.keys(statusData).map((spotId) => (
                        <div className={styles.linha_vertical} key={spotId}>
                            {statusData[spotId].map((item, index) => (
                                <div key={index} className={styles.vaga_container}>
                                <button
                                    onClick={() => handleOpenModal(item)}
                                    className={`${item.status === 'Occupied' ? styles.occupied : ''} ${styles.vaga}`}
                                ></button>
                                <p className={styles.vaga_marcacao}>{`Vaga ${spotId}`}</p>
                                {/* <p className={styles.vaga_status}>{`Status: ${item.status}`}</p> */}
                            </div>
                            ))}
                        </div>
                      ))}
                    </div>
                    <Modal isOpen={openModal} onClose={() => setOpenModal(false)} data={selectedSpot} ownerData={ownerData}/>
                </div> 
            </div>
        </>
    )
  }