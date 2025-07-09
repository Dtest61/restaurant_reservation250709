const app = Vue.createApp({
  delimiters: ['[[', ']]'], // ← これを追加！
  data() {
    return {
      showOverlay: true,
      showReservationForm: false,
      name: '',
      email: '',
      dateTime: '',
      numberOfPeople: 1,
      inquiry: '', // ← 追加
      menuItems: [
        { id: 1, name: 'お寿司', description: '新鮮なネタで作ったお寿司。', image: 'images/dish1.jpg' },
        { id: 2, name: '焼き鳥', description: 'ジューシーで美味しい焼き鳥。', image: 'images/dish2.jpg' },
        { id: 3, name: '天ぷら', description: 'サクサクの天ぷら。', image: 'images/dish3.jpg' }
      ],
      showModal: false
    };
  },
  methods: {
    hideOverlay() {
      this.showOverlay = false; // 動画が終了したらオーバーレイを非表示に
    },
    handleScroll() {
  const reservationSection = document.getElementById('reservation-section');
  if (reservationSection) {
    if (window.scrollY + window.innerHeight >= reservationSection.offsetTop) {
      this.showReservationForm = true;
    }
  }
},

   handleSubmit() {
    console.log("仮予約ボタンが押されました");
    console.log("フォーム送信：", this.name, this.email); // ← 動作確認用

    console.log("名前:", this.name);
    console.log("メール:", this.email);
    console.log("日時:", this.dateTime);
    console.log("人数:", this.numberOfPeople);
    console.log("問い合わせ:", this.inquiry);

    this.showModal = true; // モーダル表示
  },

 

  closeModal() {
    this.showModal = false;
  
    // 仮送信処理
    alert('予約内容を確認しました。後ほどスタッフよりご連絡いたします。');
  }
},

computed: {
  formattedDateTime() {
    if (!this.dateTime) return '';

    const date = new Date(this.dateTime);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const minute = String(date.getMinutes()).padStart(2, '0');

    return `${year}年${month}月${day}日 ${hour}時${minute}分`;
  }
},

  
  mounted() {
    window.addEventListener('scroll', this.handleScroll); // スクロール時に予約フォーム表示
  },
  beforeUnmount() { // ← Vue 3 正式名称
    window.removeEventListener('scroll', this.handleScroll); // イベントリスナーを削除
  }
});

// Vueインスタンスを作成して#appにマウント
app.mount('#app');