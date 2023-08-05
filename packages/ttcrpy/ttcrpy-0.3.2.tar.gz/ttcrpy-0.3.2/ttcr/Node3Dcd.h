//
//  Node3Dcd.h
//  ttcr
//
//  Created by Bernard Giroux on 2018-12-11.
//  Copyright © 2018 Bernard Giroux. All rights reserved.
//

#ifndef Node3Dcd_h
#define Node3Dcd_h

#include "Node3Dc.h"


// for temporary dynamic nodes

namespace ttcr {
    
    template<typename T1, typename T2>
    class Node3Dcd : public Node3Dc<T1,T2> {
    public:
        Node3Dcd() : Node3Dc<T1,T2>(1) {}
        
        Node3Dcd(const T1 t, const T1 xx, const T1 yy, const T1 zz, const size_t nt,
                 const size_t i) : Node3Dc<T1,T2>(t, xx, yy, zz, 1, 0) {}
        
        Node3Dcd(const Node3Dcd<T1,T2>& node) :
        Node3Dc<T1,T2>(node.tt[0], node.x, node.y, node.z, 1, 0)
        {
            this->gridIndex = node.gridIndex;
            this->owners = node.owners;
        }
        
        T1 getTT(const size_t n) const { return this->tt[0]; }
        void setTT(const T1 t, const size_t n ) { this->tt[0] = t; }
    };
    
    template<typename T1, typename T2>
    std::ostream& operator<< (std::ostream& os, const Node3Dcd<T1, T2> &n) {
        os << n.getX() << ' ' << n.getY() << ' ' << n.getZ();
        return os;
    }
    
    template<typename T1, typename T2>
    sxyz<T1> operator-(const Node3Dcd<T1,T2>& lhs, const Node3Dcd<T1,T2>& rhs) {
        return sxyz<T1>( lhs.getX()-rhs.getX(), lhs.getY()-rhs.getY(), lhs.getZ()-rhs.getZ() );
    }
    
    template<typename T1, typename T2>
    sxyz<T1> operator-(const sxyz<T1>& lhs, const Node3Dcd<T1,T2>& rhs) {
        return sxyz<T1>( lhs.x-rhs.getX(), lhs.y-rhs.getY(), lhs.z-rhs.getZ() );
    }
    
    template<typename T1, typename T2>
    sxyz<T1> operator-(const Node3Dcd<T1,T2>& lhs, const sxyz<T1>& rhs) {
        return sxyz<T1>( lhs.getX()-rhs.x, lhs.getY()-rhs.y, lhs.getZ()-rhs.z );
    }
}
#endif /* Node3Dcd_h */
