'use client';

import { useEffect, useRef, useState } from 'react';
import styles from '../../styles/JumpGame.module.css';

type StatusComponentProps = {
  onStatusChange: (status: string) => void;
};

const StatusComponent = ({ onStatusChange }: StatusComponentProps) => {
  const [status, setStatus] = useState('');

  useEffect(() => {
    const fetchStatus = async () => {
      const response = await fetch('/status.json'); // パブリックディレクトリ内のJSONファイルの相対パス
      const data = await response.json();
      setStatus(data.status);
      if (data.status === 'shake') {
        onStatusChange('shake');
      }
    };

    const intervalId = setInterval(fetchStatus, 100); // 1秒ごとにステータスをチェック

    return () => clearInterval(intervalId); // クリーンアップ
  }, [onStatusChange]);

  return (
    <div>
      <h1>Current Status: {status}</h1>
    </div>
  );
};

export default function JumpGame() {
  const playerRef = useRef<HTMLDivElement>(null);
  const obstacleRef = useRef<HTMLDivElement>(null);
  const [isJumping, setIsJumping] = useState(false);
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(0);



  const jump = () => {
    if (isJumping) return;
    setIsJumping(true);
    playerRef.current?.classList.add(styles.jump);
    setTimeout(() => {
      playerRef.current?.classList.remove(styles.jump);
      setIsJumping(false);
    }, 1000);
  };

  const handleStatusChange = (status: string) => {
    if (status === 'shake') {
      jump();
    }
  };

  const checkCollision = () => {
    if (playerRef.current && obstacleRef.current) {
      const playerRect = playerRef.current.getBoundingClientRect();
      const obstacleRect = obstacleRef.current.getBoundingClientRect();

      if (
        playerRect.right > obstacleRect.left &&
        playerRect.left < obstacleRect.right &&
        playerRect.bottom > obstacleRect.top &&
        playerRect.top < obstacleRect.bottom
      ) {
        alert('ゲームオーバー');
        if (score > highScore) {
          setHighScore(score);
          localStorage.setItem('highScore', score.toString());
        }
        setScore(0);
        location.reload();
      } else if (obstacleRect.right < playerRect.left) {
        setScore((prevScore) => prevScore + 1);
        obstacleRef.current.style.right = '0px'; // リセット位置
      }
    }
  };

  useEffect(() => {
    document.addEventListener('keydown', (event) => {
      if (event.code === 'Space') {
        jump();
      }
    });

    const storedHighScore = localStorage.getItem('highScore');
    if (storedHighScore) {
      setHighScore(parseInt(storedHighScore, 10));
    }

    const collisionInterval = setInterval(checkCollision, 10);
    return () => clearInterval(collisionInterval);
  }, [score, highScore]);

  return (
    <div className={styles.game}>
      <div ref={playerRef} className={styles.player}></div>
      <div ref={obstacleRef} className={styles.obstacle}></div>
      <div className={styles.score}>
        スコア: {score} | 最高スコア: {highScore}
      </div>
      <StatusComponent onStatusChange={handleStatusChange} />
    </div>
  );
}
