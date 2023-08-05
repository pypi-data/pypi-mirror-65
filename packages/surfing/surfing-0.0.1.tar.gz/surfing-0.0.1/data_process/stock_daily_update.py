from raw.download_rqdata_daily import DownloadRqdataDaily



if __name__ == "__main__":
    ddata = DownloadRqdataDaily(    start_date  =   '2019-01-01',
                                    end_date    =   '2019-12-20' )
    ddata.update() 
