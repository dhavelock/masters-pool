import axios from 'axios';
import { teams } from './poolinfo';

const fetchCompetitors = async () => {
  const competitors = {};

  const res = await axios.get('https://www.espn.com/golf/leaderboard');

  const rawCompetitors = parseHtml(res.data);

  rawCompetitors.forEach((competitor) => {
    competitors[competitor.name] = competitor;
  });

  return competitors;
};

const parseHtml = (raw) => {
  const startIndex = raw.search('"competitors":');
  const endIndex = raw.search(',"rawText":');
  return JSON.parse(`{${raw.substring(startIndex, endIndex)}}`).competitors;
};

const getCompetitorScore = (competitor) => {
  if (competitor == null || competitor.toPar == null) {
    return 1000;
  }
  if (competitor.detail != null && competitor.detail == 'WD') {
    return 1000;
  }
  if (competitor.cut != null && competitor.cut) {
    return 1000;
  }

  const rawScore = competitor.toPar;

  if (rawScore === 'E') {
    return 0;
  } else if (!isNaN(rawScore)) {
    return +rawScore;
  } else {
    return 1000;
  }
};

const calculateScore = (team) => {
  let score = 0;
  for (let i = 0; i < 4; i++) {
    score += getCompetitorScore(team.rosterData[i]);
  }
  return score;
};

const updateScore = (team, competitors) => {
  let rosterData = [];
  team.roster.forEach((player) => {
    const competitor =
      competitors[player] === undefined ? null : competitors[player];
    rosterData.push(competitor);
  });

  rosterData.sort((p1, p2) => {
    return getCompetitorScore(p1) - getCompetitorScore(p2);
  });

  team['rosterData'] = rosterData;
  team['score'] = calculateScore(team);
};

const getLeaderboard = async () => {
  const competitors = await fetchCompetitors();
  teams.forEach((team) => updateScore(team, competitors));
  teams.sort((t1, t2) => t1.score - t2.score);

  return teams;
};

export { getLeaderboard };
