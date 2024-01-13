document.addEventListener('DOMContentLoaded', function () {
    const mountScoreInput = document.getElementById('id_mount_score');
    const opponentScoreInput = document.getElementById('id_opponent_score');
    const mountWinCheckbox = document.getElementById('id_mount_win');

    function updateCheckbox() {
        const mountScore = parseInt(mountScoreInput.value) || 0;
        const opponentScore = parseInt(opponentScoreInput.value) || 0;
        mountWinCheckbox.checked = mountScore > opponentScore;
    }

    mountScoreInput.addEventListener('input', updateCheckbox);
    opponentScoreInput.addEventListener('input', updateCheckbox);
});
