/**
 * Web Audio API を用いた自動演奏ピアノBGMジェネレーター
 * 穏やかで心が落ち着くコード進行とアルペジオを無限に生成します。
 */
export class PianoBGM {
  constructor() {
    this.ctx = null;
    this.isPlaying = false;
    this.delayNode = null;
    this.feedbackNode = null;
    this.nextNoteTime = 0;
    this.sequenceStep = 0;
    this.timerId = null;
    
    // コード進行の定義 (Fmaj7 -> Cmaj7 -> G6 -> Am7)
    // 低音ルートと、高音のメロディ用ノート候補
    this.chords = [
      { root: 41, notes: [41, 48, 52, 57, 60, 64, 67, 72] }, // Fmaj7 (F2, C3, E3, A3, C4, E4, G4, C5)
      { root: 48, notes: [48, 55, 59, 64, 67, 71, 74, 76] }, // Cmaj7 (C3, G3, B3, E4, G4, B4, D5, E5)
      { root: 43, notes: [43, 50, 55, 59, 62, 67, 71, 74] }, // G6 (G2, D3, G3, B3, D4, G4, B4, D5)
      { root: 45, notes: [45, 52, 57, 60, 64, 67, 72, 76] }  // Am7 (A2, E3, A3, C4, E4, G4, C5, E5)
    ];
    this.currentChordIndex = 0;
  }

  start() {
    if (this.isPlaying) return;
    
    // AudioContext の初期化 (ユーザーインタラクションの後に実行される)
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioContextClass();
    this.isPlaying = true;
    
    // ディレイエフェクトの構築（ピアノの反響・響きをシミュレート）
    this.delayNode = this.ctx.createDelay(2.0);
    this.delayNode.delayTime.value = 0.6; // 600ms 遅延
    
    this.feedbackNode = this.ctx.createGain();
    this.feedbackNode.gain.value = 0.45; // 反響音の減衰
    
    // ディレイフィードバック接続
    this.delayNode.connect(this.feedbackNode);
    this.feedbackNode.connect(this.delayNode);
    
    // 出力先への接続
    this.delayNode.connect(this.ctx.destination);
    
    // スケジューラの開始
    this.nextNoteTime = this.ctx.currentTime + 0.1;
    this.sequenceStep = 0;
    this.currentChordIndex = 0;
    this.scheduler();
  }

  stop() {
    this.isPlaying = false;
    if (this.timerId) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
    if (this.ctx) {
      this.ctx.close();
      this.ctx = null;
    }
  }

  midiToFreq(note) {
    return 440 * Math.pow(2, (note - 69) / 12);
  }

  playNote(note, time, velocity = 0.5) {
    if (!this.ctx || !this.isPlaying) return;

    // ピアノの打鍵音（アタック）と胴鳴りをシミュレートするため、
    // サイン波（基本波）と少量の三角波（温かみのある倍音）をミックスします。
    const osc1 = this.ctx.createOscillator();
    const osc2 = this.ctx.createOscillator();
    const oscGain1 = this.ctx.createGain();
    const oscGain2 = this.ctx.createGain();
    const mainGain = this.ctx.createGain();

    osc1.type = 'sine';
    osc2.type = 'triangle';
    
    const freq = this.midiToFreq(note);
    osc1.frequency.setValueAtTime(freq, time);
    osc2.frequency.setValueAtTime(freq, time);

    // 各波形のブレンド比率
    oscGain1.gain.setValueAtTime(0.8, time);
    oscGain2.gain.setValueAtTime(0.2, time);

    // エンベロープ（音量の時間変化）
    mainGain.gain.setValueAtTime(0, time);
    // アタック: 非常に高速 (約10ms)
    mainGain.gain.linearRampToValueAtTime(velocity * 0.12, time + 0.008);
    // ディケイ/サステイン/リリース: ピアノ特有のゆっくりとした減衰 (約3秒)
    mainGain.gain.exponentialRampToValueAtTime(0.0001, time + 3.0);

    // ノードの接続
    osc1.connect(oscGain1);
    osc2.connect(oscGain2);
    
    oscGain1.connect(mainGain);
    oscGain2.connect(mainGain);
    
    // ドライ音（直接）とウェット音（ディレイ）の両方に送る
    mainGain.connect(this.ctx.destination);
    mainGain.connect(this.delayNode);

    // 発音
    osc1.start(time);
    osc2.start(time);
    
    // 3.1秒後にオシレーターを停止してリソースを解放
    osc1.stop(time + 3.1);
    osc2.stop(time + 3.1);
  }

  scheduler() {
    if (!this.isPlaying || !this.ctx) return;

    // 現在時間から少し先（300ms先）までの音符を予約しておく（ブラウザのタイマーのズレを防ぐため）
    while (this.nextNoteTime < this.ctx.currentTime + 0.3) {
      this.scheduleNextEvent(this.sequenceStep, this.nextNoteTime);
      this.advanceStep();
    }
    
    // 50msごとにスケジューラを再帰呼び出し
    this.timerId = setTimeout(() => this.scheduler(), 50);
  }

  advanceStep() {
    // テンポ: 1拍あたり1.2秒 (BPM 50)。心が落ち着く非常にゆったりとしたテンポ。
    const secondsPerBeat = 1.2;
    this.nextNoteTime += secondsPerBeat;
    this.sequenceStep = (this.sequenceStep + 1) % 16; // 16拍（4小節）で1ループ
  }

  scheduleNextEvent(step, time) {
    // 16拍（4小節）ごとにコードを切り替える
    if (step === 0) {
      this.currentChordIndex = (this.currentChordIndex + 1) % this.chords.length;
    }

    const chord = this.chords[this.currentChordIndex];

    // 1. 低音（伴奏）の打鍵
    // 1小節目の1拍目と、3小節目の1拍目（step 0 と step 8）に低音ルートと5度を優しく弾く
    if (step === 0) {
      this.playNote(chord.root, time, 0.4); // ルート音 (F2, C3, G2, A2)
      this.playNote(chord.root + 7, time + 0.05, 0.2); // 5度上の音 (C3, G3, D3, E3)
    } else if (step === 8) {
      this.playNote(chord.root + 12, time, 0.3); // 1オクターブ上のルート
    }

    // 2. 高音（メロディ/アルペジオ）の打鍵
    // 静寂を大切にするため、すべての拍で鳴らすのではなく、確率的かつまばらに演奏する
    const isStrongBeat = step % 4 === 0; // 小節の頭
    const isWeakBeat = step % 2 === 0;   // 拍の頭

    if (isStrongBeat) {
      // 小節の頭は高確率で高音コードトーンを弾く
      if (Math.random() < 0.8) {
        const highNotes = chord.notes.filter(n => n >= 57 && n <= 72); // A3 〜 C5 程度
        const note = highNotes[Math.floor(Math.random() * highNotes.length)];
        this.playNote(note, time, 0.25);
      }
    } else if (isWeakBeat) {
      // その他の拍の頭は50%の確率
      if (Math.random() < 0.5) {
        const highNotes = chord.notes.filter(n => n >= 60 && n <= 76); // C4 〜 E5 程度
        const note = highNotes[Math.floor(Math.random() * highNotes.length)];
        // 少し発音を遅らせて、揺らぎ（ルバート）を表現する
        const humanizeDelay = Math.random() * 0.08;
        this.playNote(note, time + humanizeDelay, 0.2);
      }
    } else {
      // 拍の裏など：稀に小さな装飾音を入れる (15%の確率)
      if (Math.random() < 0.15) {
        const highNotes = chord.notes.filter(n => n >= 64); // E4以上
        const note = highNotes[Math.floor(Math.random() * highNotes.length)];
        this.playNote(note, time, 0.12);
      }
    }
  }
}
