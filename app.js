(function () {
  const voiceMap = { en: 'en-IN', hi: 'hi-IN', te: 'te-IN' };
  const reminderPhrases = {
    en: (r) => `It is time for ${r.medicine}, ${r.dosage}. ${r.instructions || ''}`,
    hi: (r) => `अब ${r.medicine}, ${r.dosage} लेने का समय है। ${r.instructions || ''}`,
    te: (r) => `ఇప్పుడు ${r.medicine}, ${r.dosage} తీసుకునే సమయం. ${r.instructions || ''}`
  };
  const banner = document.getElementById('reminderBanner');
  const spoken = new Set();

  function speak(text, language) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = voiceMap[language] || 'en-IN';
    utterance.rate = 0.9;
    utterance.volume = 1;
    window.speechSynthesis.speak(utterance);
  }

  document.querySelectorAll('.voice-btn').forEach((button) => {
    button.addEventListener('click', () => speak(button.dataset.text || '', button.dataset.voice || 'en'));
  });

  document.querySelectorAll('[data-fill]').forEach((button) => {
    button.addEventListener('click', () => {
      const input = document.getElementById('chatMessage');
      if (input) { input.value = button.dataset.fill || ''; input.focus(); }
    });
  });

  async function pollReminders() {
    try {
      const response = await fetch('/api/reminders', { headers: { 'Accept': 'application/json' } });
      if (!response.ok) return;
      const data = await response.json();
      if (!data.reminders || !data.reminders.length) return;

      const active = data.reminders.find((r) => !spoken.has(String(r.id) + ':' + r.time));
      if (!active) return;
      const key = String(active.id) + ':' + active.time;
      spoken.add(key);
      const language = voiceMap[active.language] ? active.language : 'en';
      const prefix = active.status === 'escalated' ? {
        en: 'This reminder has been escalated. ',
        hi: 'यह रिमाइंडर एस्केलेट किया गया है। ',
        te: 'ఈ రిమైండర్ ఎస్కలేట్ చేయబడింది. '
      }[language] : '';
      const text = prefix + (reminderPhrases[language] || reminderPhrases.en)(active);
      speak(text, active.language);
      if (banner) {
        banner.hidden = false;
        banner.textContent = `Reminder: ${active.medicine} ${active.dosage} · ${active.status}`;
        setTimeout(() => { banner.hidden = true; }, 12000);
      }
    } catch (err) {
      // Background reminder checks should never stop the page from working.
    }
  }

  pollReminders();
  setInterval(pollReminders, 30000);
})();
