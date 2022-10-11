import React from "react";
import { useState, useEffect } from "react";
import classes from "./History.module.css";

import {
    DataTable,
    TableBody,
    DataTableCell,
    DataTableColumnHeader,
    TableFoot,
    TableHead,
    DataTableRow,
    Button,
    Switch,
} from '@dhis2/ui'

export function Inventory(props) {
    const d = new Date()
    const currentYearAndMonth = d.getFullYear() + '-' + d.getMonth()
    const minYearAndMonth = parseInt(d.getFullYear())-1 + '-' + d.getMonth()
    const [high, setHigh] = useState(props.high)
    const [date, setDate] = useState(props.year + '-' + props.month)
    const [warning, setWarning] = useState(props.low)
    const [error, setError] = useState(props.critical)

    function switchChanged(func, check){
        func(!check)
        // if(setColor){
        //     func(!check)
        // }
    }

    useEffect(() => {
        var regex = /^202[01]-((0\d)|(1[012]))$/g
        if(regex.test(date)) {
            props.updateYear(date.split('-')[0])
            props.updateMonth(date.split('-')[1])
            console.log('date, refesh')
        }
        else {
            console.log('invalid month' + date)
        }
    }, [date])

    if (props.mergedData) {
        return (
            <div style={{padding: '20px'}}>
                <div className='grid-in-browse'>
                    <h1>
                        Inventory
                    </h1>
                    <div style={{paddingBottom: '2vh'}}>
                        <label htmlFor='start'>Choose Month:</label>
                        <br/>
                        <input type="month" id="start" name="start"
                               min={minYearAndMonth} max={currentYearAndMonth} value={date} placeholder='YYYY-MM' onChange={(event) => {

                            console.log('change: ' + event.currentTarget.value)
                            setDate(event.currentTarget.value)

                        }}>

                        </input>
                    </div>
                    <div>
                        <h3 style={{margin: '0px'}}>Filter by stock: </h3>
                        <p style={{fontSize: '10px', margin: '0px', padding: '0px'}}>Only display commodities within the marked category. Also color code commodities.</p>
                    </div>
                    {/* <div> */}
                        <Switch checked={high} label='High' onChange={() => switchChanged(setHigh, high)}/>
                        <Switch checked={warning} warning={warning} label='Low' onChange={() => switchChanged(setWarning, warning)}/>
                        <Switch checked={error} error={error} label='Critical' onChange={() => switchChanged(setError, error)}/>
                    {/* </div> */}
                </div>
                <br/>
                <div className={classes.main}>
                <DataTable
                    layout='fixed'
                    scrollHeight='75vh'
                >
                    <TableHead>
                        <DataTableRow>
                            <DataTableColumnHeader fixed top='0'>
                                Commodity
                            </DataTableColumnHeader>
                            <DataTableColumnHeader fixed top='0'>
                                ID
                            </DataTableColumnHeader>
                            <DataTableColumnHeader fixed top='0'>
                                Consumption
                            </DataTableColumnHeader>
                            <DataTableColumnHeader fixed top='0'>
                                End Balance
                            </DataTableColumnHeader>
                            <DataTableColumnHeader fixed top='0'>
                                Quantity to be ordered
                            </DataTableColumnHeader>
                        </DataTableRow>
                    </TableHead>
                    <TableBody>
                        {props.mergedData.map(row => {
                            let rowStyle = ''
                            let critical = false;
                            
                            if(!high && !error && !warning){

                            }
                            else{
                                if((parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) >= 10) {
                                    if(!error) {
                                        return
                                    }
                                    rowStyle = 'crimson'
                                }
                                
                                else if((parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) < 5) {
                                    if(!high) {
                                        return
                                    }
                                    rowStyle = 'blue'
                                }
                                else if((parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) >= 5 && (parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) < 10) {
                                    if(!warning) {
                                        return
                                    }
                                    rowStyle = 'gold'
                                }
                            }
                            return (
                                <DataTableRow key={row.id}>
                                    <DataTableCell className={rowStyle}> {row.name} </DataTableCell>
                                    <DataTableCell className={rowStyle}> {row.id} </DataTableCell>
                                    <DataTableCell className={rowStyle}> {row.consumption} </DataTableCell>
                                    <DataTableCell className={rowStyle}> {row.endBalance} </DataTableCell>
                                    <DataTableCell className={rowStyle}> {row.quantityToBeOrdered} </DataTableCell>
                                </DataTableRow>
                            )
                        })}
                    </TableBody>
                </DataTable>
            </div>
            </div>
        )
    }
}