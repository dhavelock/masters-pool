import { getLeaderboard } from '@/fetchScores';

const Home = ({ leaderboard }) => {
  return (
    <main>
      <div>
        <h1>Masters Pool 2023</h1>
        <table className="table table-striped">
          <tbody>
            {leaderboard.map((team) => {
              return (
                <tr key={team.name}>
                  <td key={team.score}>{team.score}</td>
                  <td className="border-right" key={team.name}>
                    {team.name}
                  </td>
                  {team.rosterData.map((competitor) => {
                    if (competitor == null) {
                      return (
                        <>
                          <td className="hide-mobile" key={0}>
                            -
                          </td>
                          <td className="hide-mobile" key={1}>
                            -
                          </td>
                        </>
                      );
                    }
                    return (
                      <>
                        <td className="hide-mobile" key={competitor.guid}>
                          {competitor.toPar}&nbsp;
                        </td>
                        <td className="hide-mobile">
                          {competitor.name.substring(0, 1)}.&nbsp;
                          {competitor.lastNm}
                        </td>
                      </>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </main>
  );
};

export async function getServerSideProps() {
  // Fetch data from external API
  const leaderboard = await getLeaderboard();

  // Pass data to the page via props
  return { props: { leaderboard } };
}

export default Home;
