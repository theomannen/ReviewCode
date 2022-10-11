import React from "react";
import "./style.css";
import {
    Card,
    Box,
    DataTable,
	TableBody,
	DataTableCell,
    DataTableHead,
	TableCellHead,
    DataTableColumnHeader,
	TableHead,
	DataTableRow,
} from '@dhis2/ui'

export function InventoryCard(props){
    let headStyle = 'center pointer'
    
    switch (props.title) {
        case 'Critical':
            headStyle += ' crimson'
            break;
        
        case 'Low':
            headStyle += ' gold'
            break;

        case 'High':
            headStyle += ' blue'
            break;

        default:
            break;
    }

    console.log(headStyle)

    return (
        <Box>
            <Card className={headStyle}>
                <h2>{props.title}</h2>
                <div className='table'>
                <DataTable
                    layout="fixed"
                    scrollHeight="30vh"
                    // className='table'
                >
                    <TableHead>
                        <DataTableRow>
                            <DataTableCell className='headerCell'>
                                <label className='pointer'>Commodity</label>
                            </DataTableCell>
                            <DataTableCell align='center' className='headerCell'>
                                <label className='pointer'>Stock</label>
                            </DataTableCell>
                        </DataTableRow>
                    </TableHead>
                    <TableBody>
                    {props.mergedData.map(row => {
                        switch (props.title) {
                            case 'Critical':
                                if ((parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) < 10) {
                                    return
                                }
                                break;

                            case 'Low':
                                if (((parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) > 10) || ((parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) < 5)) {
                                    return
                                }
                                break;

                            case 'High':
                                if ((parseInt(row.consumption) + parseInt(row.endBalance))/parseInt(row.endBalance) >= 5) {
                                    return
                                }
                                break;

                            default:
                                break;
                        }
                        return (
                            <DataTableRow key={row.name}>
                                <DataTableCell>
                                    <label className='pointer'>{row.name}</label>
                                </DataTableCell>
                                <DataTableCell align='center'>
                                    <label className='pointer'>{row.endBalance}/{parseInt(row.endBalance)+parseInt(row.consumption)}</label>
                                </DataTableCell>
                            </DataTableRow>
                        )
                    })}
                    </TableBody>
                </DataTable>
                </div>
            </Card>
        </Box>
    )
}