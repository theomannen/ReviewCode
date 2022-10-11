import java.util.Arrays;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.locks.ReentrantLock;

class RadixSort {

    // The number of bits used to represent a single digit
    int useBits, cores, max, shift;
    int[] a, b, digitFrequencies, digitPointers;
    CyclicBarrier cb;
    ReentrantLock lock;


    RadixSort(int useBits) {
        this.useBits = useBits;
        this.lock = new ReentrantLock();
    }

    // Counting sort. A stable sorting algorithm.
    private void countingSort(int mask, int shift) {

        // STEP B : Count the number of occurrences of each digit in a specific position.
        double stepb = System.nanoTime();
        digitFrequencies = new int[mask + 1];
        for (int num : a)
        digitFrequencies[(num >> shift) & mask]++;

        // {System.out.println("Time full b: " + (System.nanoTime()-stepb)/1000000);}

        // STEP C : Find the start position of each digit in array B.
        digitPointers = new int[mask + 1];
        for (int i = 0; i < digitFrequencies.length - 1; i++)
        digitPointers[i + 1] = digitPointers[i] + digitFrequencies[i];

        // STEP D : Place the numbers in array A, in the correct places of array B
        // The ++ increments the digit in the pointer.
        for (int num : a)
        b[digitPointers[(num >> shift) & mask]++] = num;

    }

    // Radix sort. Uses counting sort for each position.
    int[] radixSort(int[] unsortedArray) {

        a = unsortedArray;
        b = new int[a.length];

        // STEP A : Find the maximum value.
        int max = a[0];

        for (int num : a)
        if (num > max)
        max = num;


        // Substep: Finding number of bits that is needed to represent max value
        int numBitsMax = 1;
        while (max >= (1L << numBitsMax))
        numBitsMax++;


        // Substep: Finding the number of positions needed to represent the max value
        int numOfPositions = numBitsMax / useBits;
        if (numBitsMax % useBits != 0) numOfPositions++;


        // Substep: If useBits is larger than numBitsMax,
        // set useBits equal to numBitsMax to save space.
        if (numBitsMax < useBits) useBits = numBitsMax;


        // Substep: Creating the mask and initialising the shift variable,
        // both of whom are used to extract the digits.
        int mask = (1 << useBits) - 1;
        int shift = 0;

        // Performing the counting sort on each position

        for (int i = 0; i < numOfPositions; i++) {

            countingSort(mask, shift);
            shift += useBits;

            // Setting array a to be the array to be sorted again
            int[] temp = a;
            a = b;
            b = temp;

        }
        return a;

    }
}

class ThreadRadix {

    int useBits, numOfPositions, cores, mask, max;
    int[] globalA, globalB, sumCount;
    int[][] allCount;
    CyclicBarrier cb, sync;
    ReentrantLock lock;

    ThreadRadix(int[] a, int useBits, int cores) {
        this.globalA = a;
        this.globalB = new int[a.length];
        this.useBits = useBits;
        this.cores = (cores == 0) ? Runtime.getRuntime().availableProcessors() : cores;
        this.allCount = new int[this.cores][];
        this.lock = new ReentrantLock();
        cb = new CyclicBarrier(this.cores + 1);
        sync = new CyclicBarrier(this.cores);
    }

    synchronized void updateGlobalMax(int n) {
        if (max < n) {
            max = n;
        }
    }

    // Thread worker
    class Worker implements Runnable {

        int id, step, maskStart, maskEnd, listStart, listEnd, shift, mask, localMax;
        int[] a, b, count;

        public Worker(int id, int[] a, /*int[] b,*/ int listStart, int listEnd) {
            this.id = id;
            this.a = a;
            this.b = b;
            this.listStart = listStart;
            this.listEnd = (this.id == cores - 1) ? a.length : listEnd;
            this.shift = 0;
        }

        void setMaskStartEnd(int maskStart, int maskEnd, int mask) {
            this.maskStart = maskStart;
            this.maskEnd = (id == cores - 1) ? mask + 1 : maskEnd;
            this.mask = mask;
        }

        public void run() {

//========================================Step A==========================================================================

            for (int i = listStart; i < listEnd; i++) {
                if (a[i] > localMax) {
                    localMax = a[i];
                }
            }
            updateGlobalMax(localMax);


            //Release main thread
            try {
                cb.await();
            }catch(Exception e){
                e.printStackTrace();
            }

            //Wait for main thread to calculate numOfPositions and other variables
            try {
                cb.await();
            }catch(Exception e){
                e.printStackTrace();
            }

            for (int x = 0; x < numOfPositions; x++) {
//========================================Step B==========================================================================

                // Step B is made based on material from the subject website.
                count = new int[mask + 1];

                try {
                    sync.await();
                }catch(Exception e){
                    e.printStackTrace();
                }

                // Create local versions of global arrays for fast access.
                int[] test_a = globalA;
                int[] test_b = globalB;

                for (int i = listStart; i < listEnd; i++) {
                    count[(test_a[i] >> shift) & this.mask]++;
                }

                allCount[id] = count;

                try {
                    sync.await();
                }catch(Exception e){
                    e.printStackTrace();
                }

                for (int j = maskStart; j < maskEnd; j++) {
                    int hold = 0;
                    for (int i = 0; i < cores; i++) {
                        hold += allCount[i][j];
                    }
                    sumCount[j] = hold;
                }

                try {
                    sync.await();
                }catch(Exception e){
                    e.printStackTrace();
                }


//========================================Step C==========================================================================
                /*
                For step C I decided to implement one pointer array per Thread.
                This is done to make the parralellisation of Step D somewhat easier.
                Each pointer threads position array is based on the original sequential solution,
                but is increased based on how many of the same position is found in the "earlier"
                threads. That is to say, thread of a lower ID.
                By doing this I can assure that no collision may occur.
                This also makes the sort an in-place alogrithm.
                */
                int[] pointers = new int[count.length];

                // Sets base of pointers
                for (int i = 0; i < count.length-1; i++) {
                    pointers[i + 1] = pointers[i] + sumCount[i];
                }

                // adds the count of threads of smaller id's, so as to skip over those indexes in the array b when performing step D
                for (int j = 0; j < id; j++) {
                    for (int i = 0; i < count.length; i++) {
                        pointers[i] += allCount[j][i];
                    }
                }


//========================================Step D==========================================================================

                // No syncronisation is needed between step C and D, as the pointer arrays operate individually.

                for (int i = listStart; i < listEnd; i++) {
                    test_b[pointers[(test_a[i] >> shift) & this.mask]++] = test_a[i];
                }

                shift += useBits;

                try {
                    sync.await();
                }catch(Exception e){
                    e.printStackTrace();
                }

                // I also try to split the work of moving elements from b to a.
                for (int i = listStart; i < listEnd; i++) {
                    test_a[i] = test_b[i];
                }

            }

            //Final await, so as to resync with main thread
            try {
                cb.await();
            }catch(Exception e){
                e.printStackTrace();
            }
        }
    }


    int[] ParaRadix() {

        max = globalA[0];

        Worker[] workers = new Worker[cores];
        for (int i = 0; i < cores; i++) {
            workers[i] = new Worker(i, globalA, (globalA.length/cores) * i, (globalA.length/cores) * (i + 1));
            (new Thread(workers[i])).start();
        }

        // Wait for step A to finish
        try {
            cb.await();
        }catch(Exception e){
            e.printStackTrace();
        }

        int numBitsMax = 1;
        while (max >= (1L << numBitsMax))
        numBitsMax++;

        // Substep: Finding the number of positions needed to represent the max value
        numOfPositions = numBitsMax / useBits;
        if (numBitsMax % useBits != 0) numOfPositions++;

        // Substep: If useBits is larger than numBitsMax,
        // set useBits equal to numBitsMax to save space.
        if (numBitsMax < useBits) useBits = numBitsMax;

        // Substep: Creating the mask and initialising the shift variable,
        // both of whom are used to extract the digits.
        mask = (1 << useBits) - 1;
        sumCount = new int[mask + 1];

        for (int i = 0; i < cores; i++) {
            workers[i].setMaskStartEnd((mask/cores) * i, (mask/cores) * (i + 1), mask);
        }

        // Allows Threads to start working again
        try {
            cb.await();
        }catch(Exception e){
            e.printStackTrace();
        }

        //final await
        try {

            cb.await();

        }catch(Exception e){
            e.printStackTrace();
        }

        return globalA;
    }


}

class Main {

    // Method created to quickly see differnces in arrays
    public static void comapre(int[] a, int[] b){
        System.out.println();
        for (int i = 0; i < a.length; i++){
            System.out.println(a[i] + " - " + b[i]);
        }
    }


    public static void main(String[] args) {

        int n, seed, useBits, k;

        try {

            n = Integer.parseInt(args[0]);
            seed = Integer.parseInt(args[1]);
            useBits = Integer.parseInt(args[2]);
            k = Integer.parseInt(args[3]);

        } catch (Exception e) {

            System.out.println("Correct usage is: java Main <n> <seed> <useBits> <cores>");
            return;

        }
        // Radix sorting
        int[] a = Oblig4Precode.generateArray(n, seed);
        int[] paraA = Oblig4Precode.generateArray(n, seed);

        double full = 0;
        for (int i = 0; i < 7; i++) {
            ThreadRadix tr = new ThreadRadix(paraA, useBits, k);
            double s = System.nanoTime();
            paraA = tr.ParaRadix();
            full += (System.nanoTime()-s)/1000000;
        }

        double full2 = 0;
        for (int i = 0; i < 7; i++) {
            RadixSort rs = new RadixSort(useBits);
            double s = System.nanoTime();
            a = rs.radixSort(a);
            full2 += (System.nanoTime()-s)/1000000;
        }

        System.out.println("A time: " + full2/7 + "ms");
        System.out.println("Para A time: " + full/7 + "ms");
        System.out.println("Speedup: " + (full2/full));
        int[] arraysort = Oblig4Precode.generateArray(n, seed);
        // Quick check to see if sorted (takes a few seconds at high n's)
        Arrays.sort(arraysort);
        System.out.println("Seq array is equal: " + Arrays.equals(arraysort, a));
        System.out.println("Para array is equal: " + Arrays.equals(arraysort, paraA));
    }
}
