'use client';

import { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import styles from '../styles/Home.module.css';


const StatusComponent = ({ onStatusChange }: { onStatusChange: (status: string) => void }) => {
  const [status, setStatus] = useState('');

  useEffect(() => {
    const fetchStatus = async () => {
      const response = await fetch('/status.json'); // パブリックディレクトリ内のJSONファイルの相対パス
      const data = await response.json();
      setStatus(data.status);
      if (data.status === 'tapped') {
        onStatusChange('tapped');
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
export default function Home() {
  return (
    <div className={styles.container}>
      <h1>Welcome to the Jump Game</h1>
      <Link href="/jump-game">Start Game</Link>
    </div>
  );
}
