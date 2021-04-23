import pandas as pd
import plotnine as pt


def dataCleaning():
    PakPopulation = pd.read_csv("Data_Extract_From_Health_Nutrition_and_Population_Statistics.csv")
    PakPopulation['Gender']=PakPopulation['Series Name'].apply(lambda x:'Female' if 'female' in x else 'Male')
    PakPopulation['Series Name'] = PakPopulation['Series Name'].str[16:21]
    PakPopulation['Series Name'] = PakPopulation['Series Name'].str.replace(' an', '+', regex=True)
    startYear=1960
    endYear=2019
    yearsLst= list(map(str,range(startYear,endYear+1)))

    PakPopulation.loc[PakPopulation['Gender']=="Female",yearsLst]=PakPopulation[yearsLst].apply(lambda x:-x)
    print(PakPopulation)
    return PakPopulation

def dataVisualization(PakPopulation):

    pt.ggplot(pt.aes(x=PakPopulation['Series Name'],y=PakPopulation[:,'1960':'2019'],fill=PakPopulation["Gender"])) +\
             pt.geom_bar(stat ='identity')+\
             pt.scale_fill_manual(values=('#ff7129', '#d3b4d0'))+ \
    pt.scale_y_continuous(
        breaks=(-3000000, -6000000, -9000000, 0, 3000000, 6000000, 9000000),label=("3M", "6M", "9M", "0", "3M", "6M", "9M"))+\
             pt.coord_flip()+\
    pt.transition_states(
        PakPopulation['1960':'2019'],
        transition_length=1,
        state_length=2
    )+   pt.enter_fade() + pt.exit_fade() + pt.ease_aes('cubic-in-out') + pt.animate(
        fps=24,
        duration=30,
        width=500,
        height=500,
        renderer=pt.gifski_renderer('PakPopPyramid.gif')
    )

if __name__ == '__main__':
    population = dataCleaning()
    dataVisualization(population)