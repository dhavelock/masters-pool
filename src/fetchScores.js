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
    return 0;
  }

  const rawScore = competitor.toPar;

  if (isNaN(rawScore)) {
    return 0;
  } else {
    return +rawScore;
  }
};

const updateScore = (team, competitors) => {
  let score = 0;
  let rosterData = [];
  team.roster.forEach((player) => {
    const competitor =
      competitors[player] === undefined ? null : competitors[player];
    score += getCompetitorScore(competitor);

    rosterData.push(competitor);
  });

  team['rosterData'] = rosterData;
  team['score'] = score;
};

const getLeaderboard = async () => {
  const competitors = await fetchCompetitors();
  teams.forEach((team) => updateScore(team, competitors));
  teams.sort((t1, t2) => t1.score - t2.score);

  return teams;
};

export { getLeaderboard };
